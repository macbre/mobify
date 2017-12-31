# -*- coding: utf-8 -*-
"""
Support for wordpress.com blogs

https://blogvigdis.wordpress.com/sitemap.xml
https://blogvigdis.wordpress.com/2017/03/05/powierzchnia-wysp-owczych-na-sposob-farerski/
"""
import re

from mobify.source import MultiChapterSource, MobifySource


class WordpressSource(MultiChapterSource):
    """
    This will return a set of sources for each post

    @see https://blogvigdis.wordpress.com/sitemap.xml
    """
    @staticmethod
    def is_my_url(url):
        return '.wordpress.com' in url

    def get_chapters(self):
        sitemap = '{}/sitemap.xml'.format(
            re.match(r'^(https?://[^/]+)', self._url).group(1)
        )

        # use sitemap's XML as a content
        self._logger.info("Fetching XML sitemap: %s", sitemap)
        self._content = self._http.get(sitemap).text

        # <loc>https://blogvigdis.wordpress.com/2017/12/10/jolasveinar-islandzkie-mikolaje/</loc>
        links = sorted([
            link.group(1) for link in re.finditer(r'<loc>([^<]+)</loc>', self.content)
        ])

        self._logger.info('Items in XML sitemap: %d', len(links))

        return [
            WordpressPost(link)
            for link in links
            # https://blogvigdis.wordpress.com/2017/12/10/jolasveinar-islandzkie-mikolaje/
            if re.search(r'wordpress.com/\d+/\d+/\d+/.*', link)
        ]


class WordpressPost(MobifySource):
    @staticmethod
    def is_my_url(url):
        """
        This source cannot be created directly from Publisher
        """
        raise NotImplementedError

    def get_html(self):
        content = self.xpath('//*[contains(@class, "post-content")]')

        # HTML clenaup
        post = self.remove_nodes(content, [
            '*//a[img]',
            '*//xml',
            '*[@class="wpcnt"]',  # ads
            'div[@id="jp-post-flair"]',  # share bar
        ])

        html = self.get_node_html(post)
        html = re.sub(r'</?(span|a|img|em|div)[^>]*>', '', html)
        html = re.sub(r'\sstyle="[^"]+">', '>', html)

        # print(html)

        return u'<h1>{title}</h1>\n\n{content}'.format(
            title=self.get_title(),
            content=html.strip()
        )

    def get_title(self):
        # <meta property="og:title" content="Inskrypcja, a właściwie inskrypcje z Tønsberg (N A39)" />
        return self.get_node('//*[@property="og:title"]', attr='content')

    def get_author(self):
        # <meta property="og:site_name" content="Skandynawski blog Vigdis" />
        return self.get_node('//*[@property="og:site_name"]', attr='content')

    def get_language(self):
        # <meta property="og:locale" content="pl_PL" />
        return self.get_node('//*[@property="og:locale"]', attr='content').split('_')[0]
