from django.views.generic import DetailView,ListView
from django.shortcuts import get_object_or_404,render


from forum.models import Board,Post


# Create your views here.
class IndexView(ListView):
    queryset = Board.objects.filter(parent=None)
    context_object_name = 'board_list'


class BoardView(DetailView):
    model = Board
    context_object_name = 'board'


class PostView(DetailView):
    model = Post
    context_object_name = 'post'

    def get_queryset(self):
        self.board = get_object_or_404(Board, slug=self.kwargs['board'])
        return Post.objects.filter(topic__board=self.board)

