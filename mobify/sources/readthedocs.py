"""
Read The Docs materials

https://lasagne.readthedocs.io/en/latest/
"""
import re

from mobify.source import MultiChapterSource, MobifySource


class ReadTheDocsBookSource(MultiChapterSource):
    @staticmethod
    def is_my_url(url):
        return '.readthedocs.io/' in url

    @staticmethod
    def get_canonical_url(url):
        """
        Covert https://lasagne.readthedocs.io/en/latest/ to https://lasagne.readthedocs.io/

        :type url str
        :rtype str
        """
        matches = re.search(r'//([^.]+).readthedocs.io/', url)

        if matches:
            return 'https://{}.readthedocs.io/en/latest'.format(matches.group(1))
        else:
            return None

    def get_chapters(self):
        links = self.tree.xpath('//*[@aria-label="main navigation"]//a')

        url = self.get_canonical_url(self._url)
        chapters = [url] + [url + '/' + link.attrib.get('href').lstrip('/') for link in links]

        self._logger.info('Chapters: {}'.format(chapters))

        return [ReadTheDocsBookChapter(url=chapter) for chapter in chapters]


class ReadTheDocsBookChapter(MobifySource):
    @staticmethod
    def is_my_url(url):
        """
        This source cannot be created directly from Publisher
        """
        raise NotImplementedError

    def get_html(self):
        content = self.xpath('//*[@itemprop="articleBody"]')

        html = self.get_node_html(content)

        # remove headers anchor links
        html = re.sub(r'<a class="headerlink"[^<]+</a>', '', html, flags=re.MULTILINE)

        # cleanup the code snippets
        # <span class="p">(</span>
        html = re.sub(r'<span class="\w\w?">([^<]+)</span>', r'\1', html, flags=re.MULTILINE)
        html = html.replace('<span></span>', '')

        # html = re.sub(r'</?(span|a|img|em|div)[^>]*>', '', html)

        # print(html)  # import sys; sys.exit()

        return html.strip()

    def get_title(self):
        return self.get_node('//h1//text()')

    def get_author(self):
        return self.get_node('//link[@rel="top"]', attr='title')  # Lasagne 0.2.dev1 documentation

    def get_language(self):
        return 'en'
