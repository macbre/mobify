"""
Welcome to Flask

http://flask.pocoo.org/docs/0.11/
"""
import re

from mobify.source import MultiChapterSource, MobifySource


def unique(_list):
    """
    :type _list list
    :rtype list
    """
    ret = []

    for item in _list:
        if item not in ret:
            ret.append(item)

    return ret


class FlaskSource(MultiChapterSource):
    BASE = 'https://doc.rust-lang.org/book/'

    @staticmethod
    def is_my_url(url):
        return 'flask.pocoo.org' in url

    def get_chapters(self):
        links = self.tree.xpath('//div[contains(@class,"toctree-wrapper")]//a')
        chapters = unique([self._url + link.attrib.get('href').split('#')[0] for link in links])

        self._logger.info('Chapters: {}'.format(chapters))

        return [FlaskChapter(url=chapter) for chapter in chapters]


class FlaskChapter(MobifySource):
    @staticmethod
    def is_my_url(url):
        """
        This source cannot be created directly from Publisher
        """
        raise NotImplementedError

    def get_html(self):
        content = self.xpath('//*[@role="main"]')

        html = self.get_node_html(content)
        html = re.sub(r'<a class="headerlink"[^<]*</a>', '', html)
        html = re.sub(r'</?(span|a|img|em|div)[^>]*>', '', html)

        return html.strip()

    def get_title(self):
        return self.get_node('//h1')

    def get_author(self):
        return 'Flask'

    def get_language(self):
        return 'en'
