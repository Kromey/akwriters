from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe


from helpers.templatetags.frontend_extras import octicon


register = template.Library()


@register.simple_tag
def make_tree(posts, current_post=None):
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

        if post == current_post:
            line = '<li>{icon}{title} by {user} on {date}'
        else:
            line = '<li><a href="{url}">{title}</a> by {user} on {date}'

        html += line.format(
                icon=octicon('arrow-right'),
                url=reverse('forum:post', kwargs={
                    'board':post.topic.board.slug,
                    'pk':post.pk
                    }),
                title=post.subject,
                user=post.user.username,
                date='[date]',
                )

        if post.right - post.left > 1:
            html += '<ul>'
            levels.append(post.right)
            depth = len(levels)
        else:
            html += '</li>'

    html += '</ul></li>' * depth
    html += '</ul>'

    return mark_safe(html)

