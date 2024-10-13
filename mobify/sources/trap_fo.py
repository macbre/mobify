# -*- coding: utf-8 -*-
"""
Trap.fo - English version

@see https://github.com/macbre/mobify/issues/233
@see https://trap.fo/wp-sitemap.xml
@see https://trap.fo/en/the-islands-towns-and-settlements/mykines/
"""
import re

from mobify.source import MultiChapterSource, MobifySource


class TrapFoMainSource(MultiChapterSource):
    """
    This will return a set of sources for each chapter
    """
    @staticmethod
    def is_my_url(url):
        return '://trap.fo/' in url

    def get_chapters(self):
        resp = self._get_http().get('https://trap.fo/en/wp-sitemap-posts-page-1.xml')
        resp.raise_for_status()

        sitemap = resp.text

        # <loc>https://trap.fo/en/history/argisbrekka/</loc>
        for match in re.finditer(r'<loc>([^<]+)</loc>', sitemap):
            url = match.group(1)

            # <loc>https://trap.fo/en/</loc>
            if url.endswith('/en/'):
                continue

            self._logger.info(f'Chapter: {url}')

            yield TrapFoSource(url)


class TrapFoSource(MobifySource):

    @staticmethod
    def is_my_url(url):
        """
        This source cannot be created directly from Publisher
        """
        raise NotImplementedError

    def get_html(self):
        # class="entry-content clear"
        content = self.xpath('//div[contains(@class, "entry-content")]')

        # remove TOC
        # id="ez-toc-container"
        content = self.remove_nodes(content, ['//*[@id="ez-toc-container"]'])

        # <ul class="wp-block-list">
        content = self.remove_nodes(content, ['//ul[@class="wp-block-list"]'])

        # authors
        content = self.remove_nodes(content, ['//div[contains(@class, "multiple-authors-wrapper")]'])

        # cleanup
        html = self.get_node_html(content)

        html = re.sub(r'\s?<br><br>', '</p>\n\n<p>', html)
        html = re.sub(r'<img [^>]+>', '', html)
        html = re.sub(r'<p [^>]+></p>', '', html)

        # remove links
        # <a href="https://trap.fo/en/the-islands-towns-and-settlements/vagar/" data-type="page" data-id="1691">Vágar</a>
        html = re.sub(r'<a[^>]+>([^<]+)</a>', '\\1', html)

        # <h2 class="wp-block-heading">Further reading</h2>
        html = html.replace('<h2 class="wp-block-heading">Further reading</h2>', '')

        return '<h1>{title}</h1>\n\n<p><small>{author}</small><br></p>\n\n{content}'.format(
            title=self.get_title(),
            author=self.get_author(),
            content=html.strip()
        )

    def get_title(self):
        # <h1 class="entry-title" itemprop="headline">The Faroe Islands</h1>
        return self.get_node('//h1')

    def get_author(self):
        return 'trap.fo'

    def get_language(self):
        return 'en'
