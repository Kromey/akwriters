from django import template
from django.template.loader import render_to_string

register = template.Library()


@register.simple_tag
def fi_field(field, icon=None):
    if icon:
        label_width = 2
    else:
        label_width = 4

    widget_width = 12 - label_width

    context = {
            'field': field,
            'icon': icon,
            'label_width': label_width,
            'widget_width': widget_width,
            }

    return render_to_string('formhelpers/fi_field.html', context)

