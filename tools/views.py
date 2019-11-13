from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,redirect
from django.views.generic import ListView,View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView


from .models import Character,CharacterNotes,CharacterNotesAnswer,Story


# Create your views here.
class OwnedItemsMixin:
    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

class StoryListView(LoginRequiredMixin, OwnedItemsMixin, ListView):
    model = Story
    context_object_name = 'stories'

    def get_queryset(self):
        q = super().get_queryset()
        return q.order_by('title')


class StoryDetailView(LoginRequiredMixin, OwnedItemsMixin, DetailView):
    model = Story
    context_object_name = 'story'


class CharacterListView(LoginRequiredMixin, OwnedItemsMixin, ListView):
    model = Character
    context_object_name = 'characters'


class CharacterFormMixin(object):
    model = Character
    success_url = '/tools/characters/view/{id}'
    fields = ['owner','name','age','appearance',]
    context_object_name = 'character'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        try:
            # This convoluted-seeming logic is necessary because the data is in
            # an immutable QueryDict instance, rather than a simple dict
            data = kwargs['data'].copy() # make a copy, which is mutable
            data['owner'] = self.request.user.id # update owner to current user
            kwargs['data'] = data # replace original data with our updated copy
        except KeyError:
            pass

        return kwargs

    def get_context_data(self):
        context = super().get_context_data()
        context['notes'] = CharacterNotes.objects.filter(is_active=True)

        return context


class CharacterCreateView(CharacterFormMixin, LoginRequiredMixin, CreateView):
    pass


class CharacterEditView(CharacterFormMixin, OwnedItemsMixin, LoginRequiredMixin, UpdateView):
    pass


class CharacterDetailView(LoginRequiredMixin, OwnedItemsMixin, DetailView):
    model = Character
    context_object_name = 'character'


class CharacterNotesView(LoginRequiredMixin, View):
    def post(self, request, pk):
        character = Character.objects.get(owner=request.user, pk=pk)

        for field in request.POST:
            if not field.startswith('note-'):
                continue

            text = request.POST[field]

            note_id = field.split('-')[1]
            question = CharacterNotes.objects.get(pk=field.split('-')[1])

            if text:
                answer, created = CharacterNotesAnswer.objects.get_or_create(character=character, question=question)
                answer.answer = text
                answer.save()
            else:
                CharacterNotesAnswer.objects.filter(
                        character=character,
                        question=question).delete()

        return redirect('tools:character_detail', pk=character.id)

