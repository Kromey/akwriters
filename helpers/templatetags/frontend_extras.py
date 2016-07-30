from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

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

