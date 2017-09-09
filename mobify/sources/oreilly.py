# -*- coding: utf-8 -*-
import re

from mobify.source import MobifySource


class OReillySource(MobifySource):

    HEADER = u"""
<h1>{title}</h1>
<p><strong>{lead}</strong></p>
<p><small>{author} @ oreilly.com</small><br></p>
"""

    @staticmethod
    def is_my_url(url):
        # https://www.oreilly.com/ideas/the-evolution-of-devops
        return 'oreilly.com/ideas/' in url

    def get_inner_html(self):
        article = self.xpath('//*[@itemprop="articleBody"]')

        xpaths = [
            'aside',
            'div',
            'figure[@class]',
        ]
        # clean up the HTML
        article = self.remove_nodes(article, xpaths)

        html = self.get_node_html(article)

        return html

    def get_html(self):
        # add a title and a footer
        return '\n'.join([
            self.HEADER.format(title=self.get_title(), author=self.get_author(), lead=self.get_lead()).strip(),
            self.get_inner_html()
        ]).strip()

    def get_title(self):
        # <meta property="og:title" content="Radio w Poznaniu rozpoczęło nadawanie 90 lat temu" />
        return self.get_node('//meta[@property="og:title"]', attr='content').strip()

    def get_lead(self):
        # <meta property="og:description" content="90 lat temu, 24 kwietnia 1927 roku nadawanie rozpoczęła..." />
        lead = self.get_node('//meta[@property="og:description"]', attr='content').strip()

        return lead.strip() if lead else ''

    def get_author(self):
        return self.get_node('//meta[@property="article:author"]', attr='content').strip()

    def get_language(self):
        return 'en'
