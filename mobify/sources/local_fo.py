# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from mobify.source import MobifySource


class LocalFoSource(MobifySource):
    HEADER = """
<h1>{title}</h1>
<p><small>{author} @ local.fo</small><br></p>
"""

    def set_up(self):
        # avoid HTTP 406
        self._http.headers['User-Agent'] = 'Mobify (+https://github.com/macbre/mobify)'

    @staticmethod
    def is_my_url(url):
        # http://local.fo/change-indifference-active-stance-favour-pilot-whale-hunting/
        return url.startswith('http://local.fo/')

    def get_html(self):
        article = self.xpath('//div[contains(@class, "single-entry")]')

        # clean up the HTML
        xpaths = [
            '*//img',  # images
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
        # <span class="vcard author"><a class="url fn n" href="http://local.fo/author/admin/">Local.fo</a></span>
        return self.get_node('//span[contains(@class,"vcard")]/a')

    def get_language(self):
        return 'en'
