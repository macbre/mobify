"""
Learn You a Haskell for Great Good!

http://learnyouahaskell.com/chapters
"""
import re

from mobify.source import MultiChapterSource, MobifySource


class HaskellSource(MultiChapterSource):
    BASE = 'http://learnyouahaskell.com/'

    @staticmethod
    def is_my_url(url):
        return '://learnyouahaskell.com' in url

    def get_chapters(self):
        links = self.tree.xpath('//ol[@class="chapters"]/li/a')
        chapters = [self.BASE + link.attrib.get('href') for link in links]

        self._logger.info('Chapters: {}'.format(chapters))

        return [HaskellChapter(url=chapter) for chapter in chapters]


class HaskellChapter(MobifySource):
    @staticmethod
    def is_my_url(url):
        """
        This source cannot be created directly from Publisher
        """
        raise NotImplementedError

    def get_html(self):
        content = self.xpath('//*[@id="content"]')
        content = self.remove_nodes(content, ['//*[@class="footdiv"]'])

        html = self.get_node_html(content)
        html = re.sub(r'<span class="fixed">([^<]+)</span>', r'<code>\1</code>', html)
        html = re.sub(r'</?(span|a|img|em|div)[^>]*>', '', html)
        html = re.sub(r'<pre[^>]+>', '<pre>', html)  # <pre name="code" class="haskell:hs">

        html = html.replace('<p>', '</pre><p>')

        # print(html)
        return html.strip()

    def get_title(self):
        return self.get_node('//h1')

    def get_author(self):
        return 'Miran Lipovača'

    def get_language(self):
        return 'en'
