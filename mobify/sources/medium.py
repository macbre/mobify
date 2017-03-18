# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from mobify.source import MobifySource


class MediumSource(MobifySource):
    HEADER = """
<h1>{title}</h1>
<p><small>{author} @ medium.com</small><br></p>
"""

    @staticmethod
    def is_my_url(url):
        return url.startswith('https://medium.com/')

    def get_html(self):
        article = self.xpath('//div[contains(@class, "postArticle-content")]')

        # clean up the HTML
        xpaths = [
            '*//h1',  # post title
            '*//img',  # images
            '*//figcaption',  # images
            '*//figure',  # images
            '*//hr',  # lines
        ]
        article = self.remove_nodes(article, xpaths)

        html = self.get_node_html(article)

        # remove HTML tags attributes
        html = re.sub(r'<(\w+)[^>]*>', lambda match: '<{}>'.format(match.group(1)), html)

        # promote headings to the second level
        html = html.replace('h4>', 'h2>')

        # cleanup of tags
        html = re.sub('</?(a|div|section)>', '', html).strip()

        # add a title and a footer
        return '\n'.join([
            self.HEADER.format(title=self.get_title(), author=self.get_author()).strip(),
            html
        ])

    def get_title(self):
        return self.get_node('//h1').strip()

    def get_author(self):
        # <meta property="author" content="Eric Elliott">
        return self.get_node('//meta[@property="author"]', attr='content')

    def get_language(self):
        return self.get_node('//article', 'lang')
