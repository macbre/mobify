# -*- coding: utf-8 -*-
import copy
import re
from lxml import etree

from mobify.source import MobifySource


class HistmagSource(MobifySource):

    HEADER = u"""
<h1>{title}</h1>
<p><small>{author}</small><br></p>
"""

    FOOTER = u"""
<br><br>
<hr>
<p><small>Wolna licencja – ten materiał został opublikowany na licencji Creative Commons Uznanie autorstwa
Na tych samych warunkach 3.0 Polska.</small></p>

<p><small>Redakcja i autor zezwalają na jego dowolny przedruk i wykorzystanie (również w celach komercyjnych) pod
następującymi warunkami: należy wyraźnie wskazać autora materiału oraz miejsce pierwotnej publikacji –
Portal historyczny Histmag.org, a także nazwę licencji (CC BY-SA 3.0) wraz z odnośnikiem do jej postanowień.
W przypadku przedruku w internecie konieczne jest także zamieszczenie dokładnego aktywnego
odnośnika do materiału objętego licencją.</small></p>

<p><small><strong>Źródło</strong>: <a href="{url}">{url}</a></small></p>
    """

    def set_up(self):
        self._url = self.extend_url(self._url)

    @staticmethod
    def extend_url(url):
        # extend the histmag.org URL to make it a single page article
        # http://histmag.org/Margaret-Thatcher-tajfun-reform-7896;0
        if not url.endswith(';0'):
            url += ';0'

        return url

    @staticmethod
    def _cleanup(tree):
        tree = copy.copy(tree)

        # clean up the HTML
        xpaths = [
            'table',
            'p[1]',  # first paragraph
            'h4',  # "Zobacz też"
            'hr',
            'p[small]',
            'div[contains(@class, "social")]',
            'script',
            'p[@class="article-info"]',
            'p[@class="article-tags"]',
            'ul[li[a]]',
            'p[span[@class="center"]]',  # big pictures
            'p/span/a/img',  # inline pictures
            'p[iframe]',  # video
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
        html = etree.tostring(article, pretty_print=True, method="html", encoding='utf8').decode('utf8')

        # tags cleanup
        html = re.sub(r'<h2></h2>', '', html)
        html = re.sub(r'<p>\s*</p>', '', html)
        html = re.sub(r'</?(span|a|img|em|div)[^>]*>', '', html)

        # add a title and a footer
        return '\n'.join([
            self.HEADER.format(title=self.get_title(), author=self.get_author()).strip(),
            html,
            self.FOOTER.format(url=self._url).strip()
        ])

    def get_title(self):
        return self.get_node('//title').strip()

    def get_author(self):
        return self.get_node('//p[@class="article-info"]//a').strip()

    def get_language(self):
        return 'pl'
