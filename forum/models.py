from django.conf import settings
from django.db import models,transaction
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone


from .markdown import MarkdownText


class MarkdownField(models.TextField):
    def from_db_value(self, value, expression, connection, context):
        return MarkdownText(value)

    def to_python(self, value):
        return MarkdownText(value)

    def get_prep_value(self, value):
        if value is None:
            return None
        return str(value)

    def get_internal_type(self):
        return 'TextField'


class BoardCategory(models.Model):
    title = models.CharField(max_length=25)

    def __str__(self):
        return self.title


class Board(models.Model):
    category = models.ForeignKey(
            BoardCategory,
            on_delete=models.PROTECT,
            related_name='boards',
            )
    title = models.CharField(max_length=25)
    slug = models.SlugField(blank=True, max_length=25)
    description = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            self.slug = slugify(self.title)

        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('forum:board', args=(self.slug,))

    @property
    def css(self):
        return 'label label-primary'

    def __str__(self):
        return self.title

    class Meta(object):
        ordering = ('slug',)


class Topic(models.Model):
    board = models.ForeignKey(
            Board,
            on_delete=models.CASCADE,
            related_name='topics',
            )

    @property
    def op(self):
        return self.posts.first()

    @property
    def title(self):
        return self.op.subject

    @property
    def date(self):
        return self.op.date

    @property
    def user(self):
        return self.op.user

    @property
    def post_count(self):
        return self.op.reply_count + 1

    @property
    def css(self):
        return self.op.css

    def get_absolute_url(self):
        return self.op.get_absolute_url()

    def __str__(self):
        return self.title

    @transaction.atomic
    def insert_post(self, post, reply_to):
        # We need to lock the topic tree, to prevent race conditions
        if self.posts.select_for_update():
            pass

        # Make sure nobody else has updated this in the meantime
        reply_to.refresh_from_db()
        # Make room for our post
        self.posts.filter(left__gt = reply_to.left).update(left = models.F('left') + 2)
        self.posts.filter(right__gt = reply_to.left).update(right = models.F('right') + 2)

        # Now fit ourselves right into place
        post.left = reply_to.left + 1
        post.right = post.left + 1
        # Let's just make sure we have the topic set right
        post.topic = self

        post.save()


class Post(models.Model):
    user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            )
    topic = models.ForeignKey(
            Topic,
            on_delete=models.CASCADE,
            related_name='posts',
            )
    subject = models.CharField(max_length=128)
    body = MarkdownField(help_text='We use a slightly-customized version of <a data-toggle="modal" data-target="#MarkdownHelp">Markdown</a> for formatting.')
    left = models.PositiveIntegerField(default=0)
    right = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)

    @property
    def reply_count(self):
        return int((self.right - self.left - 1) / 2)

    @property
    def ancestors(self):
        ancestors = [self.topic.board]
        for post in Post.objects.filter(topic=self.topic).filter(left__lt=self.left).filter(right__gt=self.right).order_by('left'):
            ancestors.append(post)

        return ancestors

    @property
    def css(self):
        if self == self.topic.op:
            return 'label label-success'
        else:
            return 'label label-info'

    def get_absolute_url(self):
        return reverse('forum:post', args=(self.topic.board.slug, self.pk))

    def __str__(self):
        return self.subject

    def save(self, *args, **kwargs):
        if self.right <= self.left:
            self.right = self.left + 1
        return super().save(*args, **kwargs)

    class Meta(object):
        ordering = ('left',)

