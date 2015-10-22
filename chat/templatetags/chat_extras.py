from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def prosody_domain():
    return settings.PROSODY_DEFAULT_DOMAIN
