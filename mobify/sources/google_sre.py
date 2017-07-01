# -*- coding: utf-8 -*-
"""
Site Reliability Engineering / Google

https://landing.google.com/sre/book/index.html
"""
import re

from mobify.source import MultiChapterSource, MobifySource


class GoogleSRESource(MultiChapterSource):
    BASE = 'https://landing.google.com'

    @staticmethod
    def is_my_url(url):
        return url == 'https://landing.google.com/sre/book/index.html'

    def get_chapters(self):
        links = self.tree.xpath('//div[@class="content"]//li/a')
        chapters = [self.BASE + link.attrib.get('href') for link in links][1:]  # skip the link to "Table of Contents"

        self._logger.info('Chapters: {}'.format(chapters))

        return [GoogleSREChapter(url=chapter) for chapter in chapters]


class GoogleSREChapter(MobifySource):
    @staticmethod
    def is_my_url(url):
        """
        This source cannot be created directly from Publisher
        """
        raise NotImplementedError

    def get_html(self):
        content = self.xpath('//div[@class="content"]')
        html = self.get_node_html(content)

        # print(html)
        return html.strip()

    def get_title(self):
        return self.get_node('//h1').strip()

    def get_author(self):
        return 'Google SRE team'

    def get_language(self):
        return 'en'
