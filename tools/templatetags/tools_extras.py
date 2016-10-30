from django import template


from ..models import CharacterNotesAnswer


register = template.Library()


@register.simple_tag
def note_response(question, character):
    try:
        a = character.characternotesanswer_set.get(question=question)
        return a.answer
    except CharacterNotesAnswer.DoesNotExist:
        return ''

