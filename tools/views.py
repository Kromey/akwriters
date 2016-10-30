from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView


from .models import Character,CharacterNotes


# Create your views here.
class CharacterListView(LoginRequiredMixin, ListView):
    model = Character
    context_object_name = 'characters'

    def get_queryset(self):
        q = super().get_queryset()
        return q.filter(owner=self.request.user)


class CharacterFormMixin(object):
    model = Character
    success_url = '/tools/characters/view/{id}'
    fields = ['owner','name','age','appearance',]
    context_object_name = 'character'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        try:
            data = kwargs['data'].copy()
            data['owner'] = self.request.user.id
            kwargs['data'] = data
        except KeyError:
            pass

        return kwargs

    def get_context_data(self):
        context = super().get_context_data()
        context['notes'] = CharacterNotes.objects.filter(is_active=True)

        return context


class CharacterCreateView(CharacterFormMixin, LoginRequiredMixin, CreateView):
    pass


class CharacterEditView(CharacterFormMixin, LoginRequiredMixin, UpdateView):
    pass


class CharacterDetailView(LoginRequiredMixin, DetailView):
    model = Character
    context_object_name = 'character'

    def get_queryset(self):
        q = super().get_queryset()
        return q.filter(owner=self.request.user)

