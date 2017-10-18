import shlex


from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q,F,Count,Case,When,Sum,IntegerField,Min
from django.http import HttpResponse
from django.views.generic import DetailView,ListView,View
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404,render


from forum.forms import PostForm
from forum.markdown import MarkdownText
from forum.models import Board,Post


# Create your views here.

class ForumViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['board_list'] = Board.objects.select_related('category').order_by('category__title', 'slug')

        return context


class IndexView(ForumViewMixin, ListView):
    queryset = Post.objects.select_related('op', 'board', 'user').order_by('-date')[:10]
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Most Recent Posts'
        return context


class BoardView(ForumViewMixin, DetailView):
    model = Board
    context_object_name = 'board'
    topics_per_page = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        self.page = self._get_page()

        qs = self.object.posts.filter(op_id=F('id')).annotate(post_count=Count('posts')).order_by('-date')
        context['topics'] = self._paginate_queryset(qs)

        # Don't forget that internally page is 0-indexed, but it's 1-indexed out front
        if self.page > 0:
            context['prev_page'] = self.page
        if self.page < self._get_last_page():
            context['next_page'] = self.page + 2

        return context

    def _get_page(self):
        page = self.kwargs.get('page') or 1
        return int(page) - 1

    def _paginate_queryset(self, qs):
        start = self.page * self.topics_per_page
        stop = start + self.topics_per_page

        self.total_topics = qs.count()

        return qs[start:stop]

    def _get_last_page(self):
        return int(self.total_topics / self.topics_per_page)


class PostView(ForumViewMixin, DetailView):
    model = Post
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = PostForm()

        thread = self.object.op.posts.annotate(author=F('user__username'))
        if self.request.user.is_authenticated:
            # This looks fugly, but we need to annotate our Posts with their
            # "read" state for the current user, but without duplicating them
            # as a straight JOIN would. Therefore we have to use an aggregate
            # function -- in this case, Min -- to get the appropriate GROUP BY
            # clause in the query Django generates. By using Min and a Case
            # function that assigns 0 to the user and 1 to anything else, we
            # end up with a simple boolean-ish "unread" flag on each Post.
            thread = thread.annotate(
                    unread=Min(
                        Case(
                            When(readers=self.request.user, then=0),
                            default=1,
                            output_field=IntegerField(),
                            )
                        )
                    )
        context['authenticated'] = str(self.request.user.is_authenticated)
        context['thread'] = thread

        return context

    def get_queryset(self):
        self.board = get_object_or_404(Board, slug=self.kwargs['board'])
        return Post.objects.filter(board=self.board)


class SearchView(ForumViewMixin, ListView):
    model = Post
    context_object_name = 'posts'

    def _split_query_string(self, query_string):
        try:
            return shlex.split(query_string)
        except ValueError:
            # Users may not be careful about always closing quotes
            return query_string.split(' ')

    def _build_filter(self, search_terms):
        for term in search_terms:
            yield Q(body__icontains=term) | Q(subject__icontains=term)

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q', None)

        if not q:
            # No query, no results
            qs = qs.filter(subject=None)
        else:
            split_q = self._split_query_string(q)

            qs = qs.filter(*self._build_filter(split_q))

        return qs.order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Search Results'
        context['search_query'] = self.request.GET.get('q', '')
        return context


class ForumPostMixin(LoginRequiredMixin, ForumViewMixin):
    form_class = PostForm
    template_name = 'forum/post_form.html'

    def dispatch(self, *args, **kwargs):
        self.board = get_object_or_404(Board, slug=self.kwargs['board'])
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['board'] = self.board

        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.board = self.board
        return super().form_valid(form)


class TopicCreateView(ForumPostMixin, CreateView):
    form_class = PostForm
    template_name = 'forum/post_form.html'

    def form_valid(self, form):
        return super().form_valid(form)


class ReplyCreateView(ForumPostMixin, CreateView):
    form_class = PostForm
    template_name = 'forum/post_form.html'

    def dispatch(self, *args, **kwargs):
        self.reply_to = get_object_or_404(Post, pk=self.kwargs['post'])
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['post'] = self.reply_to

        return context

    def form_valid(self, form):
        resp = super().form_valid(form)
        self.reply_to.add_reply(self.object)
        return resp


class PreviewView(View):
    def post(self, request):
        md = request.POST.get('body', '')

        return HttpResponse(MarkdownText(md).html)

