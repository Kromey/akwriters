from django import template
from django.template.loader import render_to_string

from helpers.templatetags.frontend_extras import glyphicon, octicon

register = template.Library()


@register.simple_tag
def bs_field(field, icon=None, icon_type='octicon'):
    if icon:
        if icon_type == 'glyphicon':
            icon_html = glyphicon(icon)
        elif icon_type == 'octicon':
            icon_html = octicon(icon)
        else:
            raise ValueError('Unknown icon_type: {}'.format(icon_type))

        label_width = 2
    else:
        label_width = 4
        icon_html = None

    widget_width = 12 - label_width

    # Have to add the form-control tag; why can't Bootstrap just assume this??
    # Possibly worse, Django makes me manually compile it into the widget here!
    widget = field.as_widget(attrs={"class":"form-control"})

    context = {
            'field': field,
            'widget': widget,
            'icon': icon_html,
            'label_width': label_width,
            'widget_width': widget_width,
            }

    return render_to_string('helpers/bs_field.html', context)

