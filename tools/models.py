from django.conf import settings
from django.db import models
from django.utils.text import Truncator


# Create your models here.
class Story(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=127)

class Character(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    age = models.SmallIntegerField(null=True, blank=True)
    appearance = models.TextField(blank=True)

    def __str__(self):
        return '{} ({})'.format(self.name, self.owner)


class QuestionBase(models.Model):
    question = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def __str__(self):
        q = Truncator(self.question).words(5)
        return q


class CharacterNotes(QuestionBase):
    pass


class AnswerBase(models.Model):
    answer = models.TextField()

    class Meta:
        abstract = True

    def __str__(self):
        a = Truncator(self.answer).words(5)
        return a


class CharacterNotesAnswer(AnswerBase):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    question = models.ForeignKey(CharacterNotes, on_delete=models.CASCADE)

