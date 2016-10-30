from django.conf import settings
from django.db import models


# Create your models here.
class Character(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    age = models.SmallIntegerField(null=True)
    appearance = models.TextField(blank=True)


class QuestionBase(models.Model):
    question = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class CharacterNotes(QuestionBase):
    pass


class AnswerBase(models.Model):
    answer = models.TextField()

    class Meta:
        abstract = True


class CharacterNotesAnswer(AnswerBase):
    character = models.ForeignKey(Character)

