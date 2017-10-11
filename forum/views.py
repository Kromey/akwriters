import shlex


from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import DetailView,ListView,View
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404,render


from forum.forms import PostForm
from forum.markdown import MarkdownText
from forum.models import Board,Post,Topic


# Create your views here.

class ForumViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['board_list'] = Board.objects.select_related('category').order_by('category__title', 'slug')

        return context


class IndexView(ForumViewMixin, ListView):
    queryset = Post.objects.select_related('topic', 'topic__board', 'user').order_by('-pk')[:5]
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Most Recent Posts'
        return context


class BoardView(ForumViewMixin, DetailView):
    model = Board
    context_object_name = 'board'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['topics'] = self.object.topics.order_by('-pk')[:10]

        return context


class PostView(ForumViewMixin, DetailView):
    model = Post
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = PostForm()

        return context

    def get_queryset(self):
        self.board = get_object_or_404(Board, slug=self.kwargs['board'])
        return Post.objects.filter(topic__board=self.board)


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
        return super().form_valid(form)


class TopicCreateView(ForumPostMixin, CreateView):
    form_class = PostForm
    template_name = 'forum/post_form.html'

    def form_valid(self, form):
        topic = Topic(board=self.board)
        topic.save()
        form.instance.topic = topic
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
        form.instance.topic = self.reply_to.topic
        resp = super().form_valid(form)
        self.reply_to.topic.insert_post(self.object, self.reply_to)
        return resp


class PreviewView(View):
    def post(self, request):
        md = request.POST.get('body', '')

        return HttpResponse(MarkdownText(md).html)

