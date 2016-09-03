from mobify.source import MobifySource


class AosaBookSource(MobifySource):

    HEADER = u"""
<h1>{title}</h1>
<p><small>{author}</small><br></p>
"""

    @staticmethod
    def is_my_url(url):
        # http://aosabook.org/en/git.html
        return '//aosabook.org/' in url

    def get_html(self):
        article = self.xpath('//div[@class="row"]')

        # clean up the HTML
        article = self.remove_nodes(article, ['*//footer', '*//figure'])

        html = self.get_node_html(article)

        # add a title and a footer
        return '\n'.join([
            self.HEADER.format(title=self.get_title(), author=self.get_author()).strip(),
            html
        ])

    def get_title(self):
        return self.get_node('//h1').strip()

    def get_author(self):
        return self.get_node('//div[@class="hero-unit"]//p/a').strip()

    def get_language(self):
        return 'en'
