from django import template
from django.template.loader import render_to_string

register = template.Library()


@register.simple_tag
def bs_field(field, icon=None):
    if icon:
        label_width = 2
    else:
        label_width = 4

    widget_width = 12 - label_width

    # Have to add the form-control tag; why can't Bootstrap just assume this??
    # Possibly worse, Django makes me manually compile it into the widget here!
    widget = field.as_widget(attrs={"class":"form-control"})

    context = {
            'field': field,
            'widget': widget,
            'icon': icon,
            'label_width': label_width,
            'widget_width': widget_width,
            }

    return render_to_string('helpers/bs_field.html', context)

