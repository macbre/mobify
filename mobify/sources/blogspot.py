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
    SITEMAP = 'https://{blog}.blogspot.com/sitemap.xml?page={page}'

    @staticmethod
    def is_my_url(url):
        return 'blogspot.com/' in url

    def get_chapters(self):
        # fetch sitemap
        # https://havnar.blogspot.com/sitemap.xml?page=1
        blog = re.search(r'://([^.]+).blogspot.com/', self._url).group(1)
        page = 1

        posts = []

        while True:
            self._logger.info("Fetching %d sitemap page for '%s' blog", page, blog)
            sitemap = self.http.get(self.SITEMAP.format(blog=blog, page=page)).text

            # <loc>https://havnar.blogspot.com/2015/08/wybory-do-parlamentu-wysp-owczych-2015.html</loc>
            links = re.findall(r'<loc>([^<]+)</loc>', sitemap)

            # no more links found
            if not links:
                break

            for link in links:
                posts.append(link)

            page += 1

        # process all the blog posts
        self._logger.info("Found %d posts", len(posts))

        return [
            BlogSpotPost(post)
            for post in reversed(posts)
        ]


class BlogSpotPost(MobifySource):
    @staticmethod
    def is_my_url(url):
        """
        This source cannot be created directly from Publisher
        """
        raise NotImplementedError

    def get_html(self):
        # old and new skin
        content = self.xpath('//*[contains(@itemprop, "articleBody")]') or \
                  self.xpath('//div[@class="post" and script]')

        # print(content)

        # HTML clenaup
        post = self.remove_nodes(content, [
            '*//a[img]',
            '*//xml',

            # new blogpost skins
            '*//meta',
            '*//time',
            'script',
            # footer with tags
            '*[@class="post-footer"]',
            # title
            'h3',
            '*//h3',
        ])

        html = self.get_node_html(post)
        html = re.sub(r'</?(span|a|img|em|div)[^>]*>', '', html).strip()

        # print(html); print(self.get_title()); raise Exception('foo')

        return u'<h1>{title}</h1>\n\n{content}'.format(
            title=self.get_title(),
            content=html
        )

    def get_title(self):
        # <meta content='...' property='og:title'/>
        return self.get_node('//meta[@property="og:title"]', attr='content') or 'Post'

    def get_author(self):
        return 'blogspot.com'

    def get_language(self):
        return 'pl'
