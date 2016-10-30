from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView


from .models import Character


# Create your views here.
class CharacterListView(LoginRequiredMixin, ListView):
    model = Character
    context_object_name = 'characters'

    def get_queryset(self):
        q = super().get_queryset()
        return q.filter(owner=self.request.user)

