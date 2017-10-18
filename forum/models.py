from django.conf import settings
from django.db import models,transaction
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe


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


class Post(models.Model):
    user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            )
    op = models.ForeignKey(
            'self',
            null=True, default=None,
            on_delete=models.PROTECT,
            related_name='posts',
            )
    board = models.ForeignKey(
            Board,
            on_delete=models.PROTECT,
            related_name='posts',
            )
    subject = models.CharField(max_length=128)
    body = MarkdownField(help_text='<a data-toggle="modal" data-target="#MarkdownHelp"><span class="octicon octicon-markdown"></span> Markdown</a> will be used to format your post.', blank=True)
    left = models.PositiveIntegerField(default=0)
    right = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)
    readers = models.ManyToManyField(
            settings.AUTH_USER_MODEL,
            related_name='read_posts',
            )

    @property
    def reply_count(self):
        return int((self.right - self.left - 1) / 2)

    @property
    def ancestors(self):
        ancestors = [self.board]
        for post in Post.objects.filter(op_id=self.op_id).filter(left__lt=self.left).filter(right__gt=self.right).order_by('left'):
            ancestors.append(post)

        return ancestors

    @property
    def css(self):
        if self.id == self.op_id:
            return 'label label-success'
        else:
            return 'label label-info'

    @property
    def nt(self):
        if len(self.body.markdown) == 0:
            return mark_safe('<span title="No Text" class="post-nt">(nt)</span>')
        return ''

    def get_absolute_url(self):
        return reverse('forum:post', args=(self.board.slug, self.pk))

    def __str__(self):
        return self.subject

    def save(self, *args, **kwargs):
        if self.right <= self.left:
            self.right = self.left + 1
        super().save(*args, **kwargs)

        if not self.op_id and self.id:
            self.op_id = self.id
            super().save(*args, **kwargs)

    @transaction.atomic
    def add_reply(self, post):
        # We need to lock the topic tree, to prevent race conditions
        if Post.objects.filter(op_id=self.op_id).select_for_update():
            pass

        # Make sure nobody else has updated this in the meantime
        self.refresh_from_db()
        # Make room for our post
        Post.objects.filter(op_id=self.op_id).filter(left__gt = self.left).update(left = models.F('left') + 2)
        Post.objects.filter(op_id=self.op_id).filter(right__gt = self.left).update(right = models.F('right') + 2)

        # Now fit ourselves right into place
        post.left = self.left + 1
        post.right = post.left + 1
        # Let's just make sure we have the topic set right
        post.op_id = self.op_id
        post.board_id = self.board_id

        post.save()

    class Meta(object):
        ordering = ('left',)

