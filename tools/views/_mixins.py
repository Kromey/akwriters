from django.forms import ModelChoiceField


from tools.models import Character,CharacterNotes


class OwnedItemsMixin:
    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class CharacterFormMixin(object):
    model = Character
    fields = ['owner','name','age','appearance','story',]
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

    def get_form_class(self):
        form = super().get_form_class()

        class StoryChoiceField(ModelChoiceField):
            def label_from_instance(self, obj):
                return obj.title

        stories = self.request.user.story_set
        form.base_fields['story'] = StoryChoiceField(queryset=stories)

        return form

    def get_context_data(self):
        context = super().get_context_data()
        context['notes'] = CharacterNotes.objects.filter(is_active=True)

        return context


