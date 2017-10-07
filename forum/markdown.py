import bleach
from django.utils.safestring import mark_safe
import markdown
from markdown.extensions import Extension
from markdown.extensions.toc import TocExtension


class EscapeHtmlExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        # Don't process raw HTML; better for our purposes than bleach
        # https://pythonhosted.org/Markdown/release-2.6.html#safe_mode-deprecated
        del md.preprocessors['html_block']
        del md.inlinePatterns['html']


converter = markdown.Markdown(
        output_format='html5',
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.smarty',
            TocExtension(baselevel=2),
            EscapeHtmlExtension(),
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


