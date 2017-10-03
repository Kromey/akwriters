from django.views.generic import DetailView,ListView
from django.shortcuts import get_object_or_404,render


from forum.models import Board,Post


# Create your views here.

class ForumViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['board_list'] = Board.objects.filter(parent=None)

        return context


class IndexView(ForumViewMixin, ListView):
    queryset = Post.objects.select_related('topic', 'topic__board', 'user').order_by('-pk')[:5]
    context_object_name = 'recent_posts'


class BoardView(ForumViewMixin, DetailView):
    model = Board
    context_object_name = 'board'


class PostView(ForumViewMixin, DetailView):
    model = Post
    context_object_name = 'post'

    def get_queryset(self):
        self.board = get_object_or_404(Board, slug=self.kwargs['board'])
        return Post.objects.filter(topic__board=self.board)

