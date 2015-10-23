from django import template
from django.template.loader import render_to_string

register = template.Library()


@register.simple_tag
def fi_field(field, icon):
    return render_to_string('formhelpers/fi_field.html', {'field': field, 'icon': icon})

