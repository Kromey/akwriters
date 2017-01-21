from django.views.generic import ListView
from django.shortcuts import render


from forum.models import Board


# Create your views here.
class BoardView(ListView):
    queryset = Board.objects.filter(parent=None)
    context_object_name = 'board_list'

