import requests


from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


from .models import Post


#BOT_URL = settings.THE_BOT.get('webhook', '').strip().rstrip('/')
#BASE_URL = settings.THE_BOT.get('base_url', '').strip().rstrip('/')
#
#
#if BOT_URL and BASE_URL:
#    @receiver(post_save, sender=Post, dispatch_uid='notify_bot')
#    def notify_bot(sender, instance, **kwargs):
#        if instance.is_op:
#            data = {
#                    'user': instance.user.username,
#                    'topic': instance.subject,
#                    'board': instance.board.title,
#                    'url': BASE_URL + instance.get_absolute_url(),
#                    }
#            resp = requests.post(BOT_URL+'/forum_post', json=data)
#
#            if not resp.ok:
#                raise Exception(resp.content)

