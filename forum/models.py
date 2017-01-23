from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify


class Board(models.Model):
    parent = models.ForeignKey(
            'self',
            on_delete=models.CASCADE,
            blank=True,
            null=True,
            default=None,
            )
    title = models.CharField(max_length=25)
    slug = models.SlugField(blank=True, max_length=25)
    description = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            self.slug = slugify(self.title)

        return super().save(*args, **kwargs)

    class Meta(object):
        ordering = ('slug',)


class Topic(models.Model):
    board = models.ForeignKey(
            Board,
            on_delete=models.CASCADE,
            )

    @property
    def op(self):
        return self.post_set.first()

    @property
    def title(self):
        return self.op.subject

    @property
    def user(self):
        return self.op.user

    @property
    def post_count(self):
        return self.op.reply_count + 1


class Post(models.Model):
    user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            )
    topic = models.ForeignKey(
            Topic,
            on_delete=models.CASCADE,
            )
    subject = models.CharField(max_length=128)
    body = models.TextField()
    left = models.PositiveIntegerField(default=0)
    right = models.PositiveIntegerField(default=0)

    @property
    def reply_count(self):
        return int((self.right - self.left - 1) / 2)

    class Meta(object):
        ordering = ('left',)

