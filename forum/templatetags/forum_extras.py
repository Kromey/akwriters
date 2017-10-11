from django import template
from django.template.defaultfilters import date
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe


from helpers.templatetags.frontend_extras import octicon


register = template.Library()


@register.simple_tag
def make_tree(posts, current_post=None):
    levels = []
    depth = 0
    html = '<div class="post-tree">'

    for post in posts:
        try:
            while levels[-1] < post.left:
                html += '</div>'
                levels.pop()
                depth -= 1
        except IndexError:
            pass

        if post == current_post:
            label = '<span class="label label-default">{icon}{title}</span>'
        else:
            label = '<a href="{url}" class="{css}">{title}</a>'

        label = label.format(
                icon=octicon('arrow-right'),
                url=reverse('forum:post', kwargs={
                    'board':post.topic.board.slug,
                    'pk':post.pk
                    }),
                css=post.css,
                title=post.subject,
                )

        line = '<div>{label}{nt} - <span class="author">{user}</span> {date}'
        html += line.format(
                label=label,
                nt=post.nt,
                user=post.user.username,
                date=date(timezone.localtime(post.date), 'P M j \'y'),
                )

        if post.right - post.left > 1:
            #html += '<ul>'
            levels.append(post.right)
            depth = len(levels)
        else:
            html += '</div>'

    html += '</div>' * depth
    html += '</div>'

    return mark_safe(html)

