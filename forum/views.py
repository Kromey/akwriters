from django.views.generic import DetailView,ListView
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404,render


from forum.forms import PostForm
from forum.models import Board,Post,Topic


# Create your views here.

class ForumViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['board_list'] = Board.objects.select_related('category').order_by('category__title', 'slug')

        return context


class IndexView(ForumViewMixin, ListView):
    queryset = Post.objects.select_related('topic', 'topic__board', 'user').order_by('-pk')[:5]
    context_object_name = 'recent_posts'


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

    def get_queryset(self):
        self.board = get_object_or_404(Board, slug=self.kwargs['board'])
        return Post.objects.filter(topic__board=self.board)


class TopicCreateView(ForumViewMixin, CreateView):
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
        topic = Topic(board=self.board)
        topic.save()
        form.instance.topic = topic
        form.instance.user = self.request.user
        return super().form_valid(form)

