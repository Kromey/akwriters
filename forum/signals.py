import requests


from django.db.models.signals import post_save
from django.dispatch import receiver


from .models import Post


@receiver(post_save, sender=Post, dispatch_uid='notify_bot')
def notify_bot(sender, instance, **kwargs):
    with open('/tmp/signal.log', 'a') as fh:
        fh.write('{pid} {subject} {op}\n'.format(
            pid=instance.pk,
            subject=instance.subject,
            op=instance.is_op,
            ))
    if instance.is_op:
        data = {
                'user': instance.user.username,
                'topic': instance.subject,
                'board': instance.board.title,
                'url': instance.get_absolute_url(),
                }
        resp = requests.post('http://localhost:3143/forum_post', json=data)

        if not resp.ok:
            raise Exception(resp.content)

