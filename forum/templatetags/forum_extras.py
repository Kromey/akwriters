from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.simple_tag
def make_tree(posts):
    levels = []
    depth = 0
    html = '<ul>'

    for post in posts:
        try:
            while levels[-1] < post.left:
                html += '</ul></li>'
                levels.pop()
                depth -= 1
        except IndexError:
            pass

        html += '  ' * depth + '<li>' + post.subject

        if post.right - post.left > 1:
            html += '<ul>'
            levels.append(post.right)
            depth = len(levels)
        else:
            html += '</li>'

    html += '</ul></li>' * depth
    html += '</ul>'

    return mark_safe(html)

