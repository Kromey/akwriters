from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.simple_tag
def make_tree(posts):
    levels = []
    depth = 0

    print('<ul>')

    for post in posts:
        try:
            while levels[-1] < post.left:
                print('</ul></li>')
                levels.pop()
                depth -= 1
        except IndexError:
            pass

        print('  ' * depth, '<li>', post.subject)

        if post.right - post.left > 1:
            print('<ul>')
            levels.append(post.right)
            depth = len(levels)
        else:
            print('</li>')

    print('</ul></li>' * depth)
    print('</ul>')

