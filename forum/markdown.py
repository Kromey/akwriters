import bleach
from django.utils.safestring import mark_safe
import markdown
from markdown.extensions import Extension
from markdown.extensions.toc import TocExtension
from markdown.inlinepatterns import Pattern,SimpleTagPattern
from markdown.util import etree


class EscapeHtmlExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        # Don't process raw HTML; better for our purposes than bleach
        # https://pythonhosted.org/Markdown/release-2.6.html#safe_mode-deprecated
        del md.preprocessors['html_block']
        del md.inlinePatterns['html']


class EmojiExtension(Extension):
    pattern = r':(?P<emoji>[-+\w]+):'

    def extendMarkdown(self, md, md_globals):
        emoji = Emoji(self.pattern)
        md.inlinePatterns.add('emoji', emoji, '_begin')

class Emoji(Pattern):
    def handleMatch(self, m):
        emoji = m.group('emoji').strip().lower()

        img = etree.Element('img')
        img.set('src', '/static/emoji/people/{emoji}.png'.format(emoji=emoji))
        img.set('class', 'emoji')
        img.set('title', ':{emoji}:'.format(emoji=emoji))

        return img


class StrikethroughExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns.add('strikethrough', SimpleTagPattern(r'(~{2})(.+?)\2', 'del'), '_end')


class SuperscriptExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns.add('superscript', SimpleTagPattern(r'(\^)(.+?)\b', 'sup'), '_end')


class HighlightExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns.add('highlight', SimpleTagPattern(r'(={2})(.+?)\2', 'mark'), '_end')


converter = markdown.Markdown(
        output_format='html5',
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.smarty',
            TocExtension(baselevel=2),
            StrikethroughExtension(),
            SuperscriptExtension(),
            HighlightExtension(),
            EscapeHtmlExtension(),
            EmojiExtension(),
            ],
        )
linker = bleach.linkifier.Linker(callbacks=[])


class MarkdownText(object):
    def __init__(self, md):
        self.md = md

    @property
    def html(self):
        if self.md is None:
            return None

        html = converter.reset().convert(self.md)
        linked = linker.linkify(html)

        return mark_safe(linked)

    @property
    def markdown(self):
        return self.md

    def __str__(self):
        return self.md


