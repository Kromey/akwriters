from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,redirect
from django.views.generic import ListView,View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView


from tools.models import Character,CharacterNotes,CharacterNotesAnswer,Story
from ._mixins import OwnedItemsMixin


# Create your views here.

class StoryListView(LoginRequiredMixin, OwnedItemsMixin, ListView):
    model = Story
    context_object_name = 'stories'

    def get_queryset(self):
        q = super().get_queryset()
        return q.order_by('title')


class StoryDetailView(LoginRequiredMixin, OwnedItemsMixin, DetailView):
    model = Story
    context_object_name = 'story'


