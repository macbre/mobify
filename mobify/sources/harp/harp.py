"""
Support for HarpJS books

@see http://harpjs.com/
@see http://odewahn.github.io/docker-jumpstart/
@see https://github.com/macbre/mobify/issues/10
"""
import re

from mobify.source import MultiChapterSource, MobifySource


class HarpMainSource(MultiChapterSource):
    """
    This will return a set of sources for each sub page
    """
    @staticmethod
    def is_my_url(url):
        return 'github.io/' in url  # for now let's support books published on github.io

    def get_chapters(self):
        links = self.tree.xpath('//div[contains(@class, "toc-element")]/a')
        urls = [self._url + '/' + link.attrib.get('href') for link in links]

        self._logger.info('Links: {}'.format(urls))

        return [HarpChapter(url) for url in urls]


class HarpChapter(MobifySource):
    @staticmethod
    def is_my_url(url):
        """
        This source cannot be created directly from Publisher
        """
        raise NotImplementedError

    def get_html(self):
        content = self.xpath('//section[@id="content-body"]')

        # remove title and navigation
        content = self.remove_nodes(content, [
            '//div[@class="nav-buttons"]',
            '//h1'
        ])

        # tags cleanup
        html = self.get_node_html(content)
        html = re.sub(r'</?(span|a|img|em|div)[^>]*>', '', html)

        return '<h1>{title}</h1>\n\n<p><small>{author}</small><br></p>\n\n{content}'.format(
            title=self.get_title(),
            author=self.get_author(),
            content=html.strip()
        )

    def _is_the_first_chapter(self):
        return self.get_node('//a[span[contains(@class, "glyphicon-chevron-left")]]') is None  # no prev link

    def get_title(self):
        if self._is_the_first_chapter():
            return self.get_node('//title')  # Docker Jumpstart
        else:
            return self.get_node('//section//h1')  # Images: Layered filesystems

    def get_author(self):
        title = self.get_node('//header//h1/a')  # 'Docker Jumpstart by Andrew Odewahn'
        return re.search(r' by (.*)$', title).group(1)

    def get_language(self):
        return self.get_node('/html', attr='lang')
