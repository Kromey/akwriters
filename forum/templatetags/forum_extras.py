from django import template
from django.template.defaultfilters import date
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe


from helpers.templatetags.frontend_extras import octicon


register = template.Library()


@register.inclusion_tag('forum/post_tree.html')
def post_tree(post):
    return {
            'current_post': post,
            'thread': post.op.posts.all(),
            'parents': [],
            }


@register.filter
def parents(post, parent_posts):
    try:
        while parent_posts[-1] < post.left:
            yield parent_posts.pop()
    except IndexError:
        pass

    parent_posts.append(post.right)


@register.simple_tag(takes_context=True)
def close_tree(context):
    n = len(context['parents'])
    context['parents'] = []
    return mark_safe('</div>' * n)

