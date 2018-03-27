"""
Development of Further Patterns of Enterprise Application Architecture

https://martinfowler.com/eaaDev/
https://martinfowler.com/eaaDev/EventSourcing.html
"""
import re

from mobify.source import MultiChapterSource, MobifySource


class MartinFowlerSource(MultiChapterSource):
    BASE = 'https://martinfowler.com/eaaDev/'

    @staticmethod
    def is_my_url(url):
        return 'martinfowler.com' in url

    def get_chapters(self):
        links = self.tree.xpath('//div[@class="sideMenu"]//a')
        chapters = [self.BASE + link.attrib.get('href') for link in links]

        self._logger.info('Chapters: {}'.format(chapters))

        return [MartinFowlerChapter(url=chapter) for chapter in chapters]


class MartinFowlerChapter(MobifySource):
    @staticmethod
    def is_my_url(url):
        """
        This source cannot be created directly from Publisher
        """
        raise NotImplementedError

    def get_html(self):
        content = self.xpath('//*[@id="content"]')

        html = self.get_node_html(content)
        html = re.sub(r'</?(h1|img|a|div)[^>]*>', '', html)

        return html.strip()

    def get_title(self):
        return self.get_node('//h1')

    def get_author(self):
        return 'Martin Fowler'

    def get_language(self):
        return 'en'
