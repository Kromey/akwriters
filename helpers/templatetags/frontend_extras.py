from datetime import timedelta


from django import template
from django.template.loader import render_to_string
from django.template.defaultfilters import date,time
from django.utils.safestring import mark_safe
from django.utils import timezone

register = template.Library()


_span_icon = '<span class="{family} {family}-{icon}" aria-hidden="true"></span>'
_accessible_label = '<span class="sr-only">{label}</span>'


@register.simple_tag
def glyphicon(icon, label=None):
    html = _make_span_icon('glyphicon', icon)
    if label:
        html = html + _make_accessible_label(label)

    return mark_safe(html)


@register.simple_tag
def octicon(icon, label=None):
    html = _make_span_icon('octicon', icon)
    if label:
        html = html + _make_accessible_label(label)

    return mark_safe(html)


def _make_span_icon(family, icon):
    return _span_icon.format(family=family, icon=icon)

def _make_accessible_label(label):
    return _accessible_label.format(label=label)


@register.filter(expects_localtime=True, is_safe=False)
def simple_time(value):
    # timzone.now() is UTC, put it into localtime for tests
    today = timezone.localtime(timezone.now())
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)

    try:
        if today.year == value.year and today.month == value.month and today.day == value.day:
            return time(value, 'g:i A')
        if yesterday.year == value.year and yesterday.month == value.month and yesterday.day == value.day:
            return 'Yesterday'
        if tomorrow.year == value.year and tomorrow.month == value.month and tomorrow.day == value.day:
            return 'Tomorrow'
        else:
            return date(value, 'M j, Y')
    except (AttributeError, TypeError):
        return ''

