from django import template
from django.template.loader import render_to_string

register = template.Library()


_span_icon = '<span class="{family} {family}-{icon}" {style} aria-hidden="true"></span>'
_accessible_label = '<span class="sr-only">{label}</span>'


@register.simple_tag
def glyphicon(icon, label=None, style=None):
    html = _make_span_icon('glyphicon', icon, style)
    if label:
        html = html + _make_accessible_label(label)

    return html


@register.simple_tag
def octicon(icon, label=None, style=None):
    html = _make_span_icon('octicon', icon, style)
    if label:
        html = html + _make_accessible_label(label)

    return html


def _make_span_icon(family, icon, style=None):
    css = ''
    if style:
        css = 'style="{}"'.format(style)

    return _span_icon.format(family=family, icon=icon, style=css)

def _make_accessible_label(label):
    return _accessible_label.format(label=label)

