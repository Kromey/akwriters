from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView


from .models import Character


# Create your views here.
class CharacterListView(LoginRequiredMixin, ListView):
    model = Character
    context_object_name = 'characters'

    def get_queryset(self):
        q = super().get_queryset()
        return q.filter(owner=self.request.user)


class CharacterCreateView(LoginRequiredMixin, CreateView):
    model = Character
    success_url = '/tools/characters'
    fields = ['owner','name','age','appearance',]

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        try:
            data = kwargs['data'].copy()
            data['owner'] = self.request.user.id
            kwargs['data'] = data
        except KeyError:
            pass

        return kwargs

