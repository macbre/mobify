"""
The Rust Programming Language

https://doc.rust-lang.org/book/
"""
import re

from mobify.source import MultiChapterSource, MobifySource


class RustBookSource(MultiChapterSource):
    BASE = 'https://doc.rust-lang.org/book/'

    @staticmethod
    def is_my_url(url):
        return 'doc.rust-lang.org' in url

    def get_chapters(self):
        links = self.tree.xpath('//div[@id="toc"]//a')
        chapters = [self.BASE + link.attrib.get('href') for link in links]

        self._logger.info('Chapters: {}'.format(chapters))

        return [RustBookChapter(url=chapter) for chapter in chapters]


class RustBookChapter(MobifySource):
    @staticmethod
    def is_my_url(url):
        """
        This source cannot be created directly from Publisher
        """
        raise NotImplementedError

    def get_html(self):
        content = self.xpath('//div[@id="page"]')

        html = self.get_node_html(content)

        html = re.sub(r'<span class="rusttest">[^<]+</span>', '', html, flags=re.MULTILINE)
        html = re.sub(r'<script[^<]+</script>', '', html, flags=re.MULTILINE)

        html = re.sub(r'</?(span|a|img|em|div)[^>]*>', '', html)

        # print(html)

        return html.strip()

    def get_title(self):
        return self.get_node('//h1[@class="title"]')

    def get_author(self):
        return 'rust-lang.org'

    def get_language(self):
        return 'en'
