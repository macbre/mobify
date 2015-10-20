# -*- coding: utf-8 -*-
"""
Opowieści z Krypty

@see http://www.nosferatu.art.pl/files/tr3.html
"""
import re

from mobify.source import MultiChapterSource, MobifySource


class NosferatuMainSource(MultiChapterSource):
    """
    This will return a set of sources for each sub page
    """
    @staticmethod
    def is_my_url(url):
        return 'nosferatu.art.pl' in url

    def get_chapters(self):
        links = self.tree.xpath('//a[@href]')
        urls = ['http://www.nosferatu.art.pl/files/' + link.attrib.get('href') for link in links]

        self._logger.info('Links: {}'.format(urls))

        return [NosferatuSource(url) for url in urls]


class NosferatuSource(MobifySource):

    @staticmethod
    def is_my_url(url):
        """
        This source cannot be created directly from Publisher
        """
        raise NotImplementedError

    def get_html(self):
        content = self.xpath('//p[@style]')

        # cleanup
        html = self.get_node_html(content)

        html = re.sub(r'\s?<br><br>', '</p>\n\n<p>', html)
        html = re.sub(r'<img [^>]+>', '', html)
        html = re.sub(r'<p [^>]+></p>', '', html)

        return '<h1>{title}</h1>\n\n<p><small>{author}</small><br></p>\n\n{content}'.format(
            title=self.get_title(),
            author=self.get_author(),
            content=html.strip()
        )

    def get_title(self):
        return self.get_node('//font[@size]')

    def get_author(self):
        author = self.get_node('//p[@align]')
        return re.sub(r'\s+', ' ', author)

    def get_language(self):
        return 'pl'
