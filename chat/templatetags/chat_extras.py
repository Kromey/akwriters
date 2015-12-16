from django import template
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static

register = template.Library()


@register.simple_tag
def prosody_domain():
    return settings.PROSODY_DEFAULT_DOMAIN

@register.simple_tag
def chat_domain():
    return prosody_domain()

@register.simple_tag
def prosody_proto():
    # Set height and width for the image
    width = 16
    height = 16

    # The protocol itself
    proto = 'XMPP'

    # The staticfiles path to the protocol image/logo
    img = static('img/xmpp.png')

    # Now put it all together and return the result
    return '<img src="{}" alt="" class="chat-protocol" width="{}" height="{}" />{}'.format(
            img, width, height, proto)
