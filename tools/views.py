from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,redirect
from django.views.generic import ListView,View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView


from .models import Character,CharacterNotes,CharacterNotesAnswer


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

