from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,redirect
from django.views.generic import ListView,View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView


from tools.models import Character,CharacterNotes,CharacterNotesAnswer,Story
from ._mixins import CharacterFormMixin,OwnedItemsMixin


# Create your views here.

class CharacterCreateView(CharacterFormMixin, LoginRequiredMixin, CreateView):
    pass


class CharacterEditView(CharacterFormMixin, OwnedItemsMixin, LoginRequiredMixin, UpdateView):
    pass


class CharacterDetailView(LoginRequiredMixin, OwnedItemsMixin, DetailView):
    model = Character
    context_object_name = 'character'


class CharacterNotesView(LoginRequiredMixin, View):
    def post(self, request, story_id, pk):
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

        return redirect(character)

