"""
Support for blogspot.com blogs
"""
import re

from mobify.source import MultiChapterSource, MobifySource


class BlogSpotSource(MultiChapterSource):
    """
    This will return a set of sources for each month

    @see http://havnar.blogspot.com/
    """
    @staticmethod
    def is_my_url(url):
        return 'blogspot.com/' in url

    def get_chapters(self):
        links = self.tree.xpath('//ul[@class="hierarchy"]/li/a[@class="post-count-link" and contains(@href, "/search")]')
        archive = [link.attrib.get('href') for link in links]

        self._logger.info('Archive entries: {}'.format(archive))

        posts = []

        for entry in archive:
            posts += BlogSpotPostsArchive(entry).get_chapters()

        posts.reverse()  # return from the oldest to the latest blog post
        return posts


class BlogSpotPostsArchive(MultiChapterSource):
    """
    Parse per-year archive

    @see http://havnar.blogspot.com/search?updated-min=2009-01-01T00:00:00%2B01:00&updated-max=2010-01-01T00:00:00%2B01:00&max-results=24
    """
    @staticmethod
    def is_my_url(url):
        """
        This source cannot be created directly from Publisher
        """
        raise NotImplementedError

    def get_chapters(self):
        posts = self.tree.xpath('//*[@itemprop="blogPost"]')
        self._logger.info('Posts: {}'.format(len(posts)))

        chapters = []

        for post in posts:
            chapters.append(
                BlogSpotPost(
                    url='',
                    content=self.get_node_html(post)
                )
            )

        return chapters


class BlogSpotPost(MobifySource):
    @staticmethod
    def is_my_url(url):
        """
        This source cannot be created directly from Publisher
        """
        raise NotImplementedError

    def get_html(self):
        content = self.xpath('*[contains(@itemprop, "articleBody")]')

        # HTML clenaup
        post = self.remove_nodes(content, [
            '*//a[img]',
            '*//xml'
        ])

        html = self.get_node_html(post)
        html = re.sub(r'</?(span|a|img|em|div)[^>]*>', '', html)

        print(html)

        return u'<h1>{title}</h1>\n\n{content}'.format(
            title=self.get_title(),
            content=html.strip()
        )

    def get_title(self):
        return self.get_node('//*[@itemprop="name"]/a') or 'Post'

    def get_author(self):
        return 'blogspot.com'

    def get_language(self):
        return 'pl'
