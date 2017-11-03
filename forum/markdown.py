from glob import glob
import os
import re


import bleach
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.safestring import mark_safe
import markdown
from markdown.extensions import Extension
from markdown.extensions.toc import TocExtension
from markdown.inlinepatterns import Pattern,SimpleTagPattern
from markdown.preprocessors import Preprocessor
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
        md.inlinePatterns.add('emoji', emoji, '_end')

class Emoji(Pattern):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        base_dir = os.path.dirname(__file__)
        emoji_dir = os.path.join(base_dir, 'static/emoji')

        self.emoji = {}
        for dat in glob(emoji_dir + '/*/emoji.dat'):
            category = os.path.basename(os.path.dirname(dat))
            with open(dat, 'r') as fh:
                for line in fh:
                    filename, name, *aliases = re.split(r',?\s', line.strip())
                    self.emoji[name] = (category, os.path.basename(filename))

    def handleMatch(self, m):
        emoji = m.group('emoji').strip().lower()

        try:
            category, filename = self.emoji[emoji]

            src = static(os.path.join('emoji', category, filename))

            elm = etree.Element('img')
            elm.set('src', src)
            elm.set('class', 'emoji')
            elm.set('title', ':{emoji}:'.format(emoji=emoji))
        except KeyError:
            elm = etree.Element('span')
            elm.text = emoji
            elm.set('class', 'emoji emoji-unk')
            elm.set('title', 'Unrecognized emoji code ":{emoji}:"'.format(emoji=emoji))

        return elm


class EmoticonExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.preprocessors.add('emoticon', Emoticon(), '_end')

class Emoticon(Preprocessor):
    pattern = re.compile(r'(?P<emoticon>[O0>]?[:;]\'?-?[\)\(\|DPpþOo@/\\3]|(<[\\/]?3){1,2}|[>Oo][\._][<Oo]|<\("\))')

    emoticons = {
            ':)': ':simple_smile:',
            ':3': ':smile_cat:',
            ':(': ':frowning:',
            ':\')': ':joy:',
            ':\'(': ':cry:',
            ';)': ':wink:',
            ':D': ':laughing:',
            ':@': ':angry:',
            '>:@': ':rage:',
            '>:(': ':imp:',
            '>:)': ':smiling_imp:',
            'O:)': ':innocent:',
            '0:)': ':innocent:',
            ':|': ':expressionless:',
            ':P': ':stuck_out_tongue:',
            ':p': ':stuck_out_tongue:',
            ':þ': ':stuck_out_tongue:',
            ';P': ':stuck_out_tongue_winking_eye:',
            ';p': ':stuck_out_tongue_winking_eye:',
            ';þ': ':stuck_out_tongue_winking_eye:',
            ':O': ':open_mouth:',
            ':o': ':open_mouth:',
            #':/': ':confused:', #is conflicting with links at the moment
            ':\\': ':confused:',
            '<3': ':heart:',
            '<3<3': ':two_hearts:',
            '</3': ':broken_heart:',
            '<\\3': ':broken_heart:',
            '>.<': ':confounded:',
            'O_o': ':confused:',
            'O_O': ':confused:',
            'o_O': ':confused:',
            'o_o': ':confused:',
            '<(")': ':penguin:',
            }

    def run(self, lines):
        new_lines = []
        for line in lines:
            new_lines.append(self.pattern.sub(self.handleMatch, line))

        return new_lines

    def handleMatch(self, m):
        emoticon = m.group('emoticon')

        try:
            return self.emoticons[emoticon]
        except KeyError:
            try:
                return self.emoticons[emoticon.replace('-', '')]
            except KeyError:
                return emoticon


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
            EmoticonExtension(),
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


