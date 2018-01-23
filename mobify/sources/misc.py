# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
from os import getenv

from mobify.source import MobifySource


class MiscSource(MobifySource):
    """
    This source needs to be forced via --source=MiscSource
    
    and configured via env variables
    MOBIFY_SOURCE_TITLE=//h2
    MOBIFY_SOURCE_CONTENT=//article
    """

    @staticmethod
    def is_my_url(url):
        return False

    def get_html(self):
        content_xpath = getenv('MOBIFY_SOURCE_CONTENT', '//article')
        self._logger.info("Content XPath [MOBIFY_SOURCE_CONTENT]: %s", content_xpath)

        article = self.xpath(content_xpath)

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
        return '<h1>{}</h1>{}'.format(self.get_title(), html).strip()

    def get_title(self):
        title_xpath = getenv('MOBIFY_SOURCE_TITLE', '//h1')
        self._logger.info("Title XPath [MOBIFY_SOURCE_TITLE]: %s", title_xpath)

        return self.get_node(title_xpath).strip()

    def get_author(self):
        return ''

    def get_language(self):
        """
        :rtype str
        """
        return self.get_node('//html', 'lang') or 'en'
