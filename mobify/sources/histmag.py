# -*- coding: utf-8 -*-
import re
from lxml import etree

from mobify.source import MobifySource

class HistmagSource(MobifySource):

    @staticmethod
    def _cleanup(tree):
        # clean up the HTML
        xpaths = [
            'table',
            'h4',  # "Zobacz też"
            'hr',
            'p[small]',
            'div[contains(@class, "social")]',
            'script',
            'p[@class]',
            'ul[li]',
            'p[span[@class="center"]]',  # duże obrazki
            'p/span/a/img',  # obrazki
        ]

        for xpath in xpaths:
            nodes = tree.xpath(xpath)
            [node.getparent().remove(node) for node in nodes]

        return tree

    @staticmethod
    def is_my_url(url):
        return url.startswith('http://histmag.org/')

    def get_html(self):
        article = self.xpath('//*[@id="article"]')

        article = self._cleanup(article)
        html = etree.tostring(article, pretty_print=True, method="html", encoding='utf8')

        # tags cleanup
        html = re.sub(u'<h2></h2>', '', html)
        html = re.sub(u'<p>\s*</p>', '', html)
        html = re.sub(u'</?(span|a|img|em)[^>]*>', '', html)

        return html

    def get_title(self):
        return self.get_node('//title').strip()

    def get_author(self):
        return self.get_node('//p[@class="article-info"]//a').strip()

    def get_language(self):
        return 'pl'
