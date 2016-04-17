"""
Support for tumblr blogs

@see http://poznanznanyinieznany.tumblr.com/
"""
import re

from mobify.source import MultiChapterSource, MobifySource


class TumblrArchiveSource(MultiChapterSource):
    """
    Parse tumblr API archive

    @see https://api.tumblr.com/v2/blog/poznanznanyinieznany.tumblr.com/posts/text?api_key=fuiKNFp9vQFvjLNvx4sUwti4Yb5yGutBN4Xh10LXZhhRKjWlV4
    """
    API_KEY = 'fuiKNFp9vQFvjLNvx4sUwti4Yb5yGutBN4Xh10LXZhhRKjWlV4'
    LIMIT = 20  # posts per page

    @staticmethod
    def is_my_url(url):
        return '.tumblr.com/' in url

    def get_chapters(self):
        # http://poznanznanyinieznany.tumblr.com/ -> poznanznanyinieznany.tumblr.com
        host = re.search(r'//([^/]+)/', self._url).group(1)

        posts = []
        offset = 0

        while True:
            self._logger.info('Offset #{}'.format(offset))

            url = 'https://api.tumblr.com/v2/blog/{}/posts/text?api_key={}&limit={}&offset={}'.\
                format(host, self.API_KEY, self.LIMIT, offset)

            resp = self._http.get(url).json()

            # no more posts found
            if len(resp['response']['posts']) == 0:
                break

            posts += resp['response']['posts']
            offset += self.LIMIT

        self._logger.info('Posts: {}'.format(len(posts)))
        chapters = []

        # let's start from the oldest posts
        for post in reversed(posts):
            chapters.append(
                TumblrPost(
                    url='',
                    content=post  # pass the post data from API response
                )
            )

        return chapters


class TumblrPost(MobifySource):
    @staticmethod
    def is_my_url(url):
        """
        This source cannot be created directly from Publisher
        """
        raise NotImplementedError

    def get_html(self):
        html = self._content['body']
        html = re.sub(r'</?(figure|img)[^>]*>', '', html)

        return u'<h1>{title}</h1>\n\n{content}'.format(
            title=self._content['title'],
            content=html
        )

    def get_title(self):
        return self._content['title'] or 'post'

    def get_author(self):
        return self._content['blog_name']

    def get_language(self):
        return 'pl'
