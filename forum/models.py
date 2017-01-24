from django.conf import settings
from django.db import models,transaction
from django.template.defaultfilters import slugify


class Board(models.Model):
    parent = models.ForeignKey(
            'self',
            on_delete=models.CASCADE,
            blank=True,
            null=True,
            default=None,
            related_name='sub_boards',
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
            related_name='topics',
            )

    @property
    def op(self):
        return self.posts.first()

    @property
    def title(self):
        return self.op.subject

    @property
    def user(self):
        return self.op.user

    @property
    def post_count(self):
        return self.op.reply_count + 1

    @transaction.atomic
    def insert_post(self, post, reply_to):
        # We need to lock the topic tree, to prevent race conditions
        if Post.objects.select_for_update().filter(topic=self):
            pass

        # Make sure nobody else has updated this in the meantime
        reply_to.refresh_from_db()
        # Make room for our post
        Post.objects.filter(topic=self).filter(left__gt = reply_to.left).update(left = models.F('left') + 2)
        Post.objects.filter(topic=self).filter(right__gt = reply_to.left).update(right = models.F('right') + 2)

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
    body = models.TextField()
    left = models.PositiveIntegerField(default=0)
    right = models.PositiveIntegerField(default=0)

    @property
    def reply_count(self):
        return int((self.right - self.left - 1) / 2)

    class Meta(object):
        ordering = ('left',)

