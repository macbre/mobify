# -*- coding: utf-8 -*-
import re
try:
    from urllib import quote  # Py 2.x
except ImportError:
    from urllib.parse import quote  # Py 3.x

from mobify.source import MobifySource


class WikipediaSource(MobifySource):

    HEADER = u"""
<h1>{title}</h1>
<p><small>Z Wikipedii, wolnej encyklopedii</small><br></p>
"""

    FOOTER = u"""
<br><br>
<hr>
<p><small>Tekst udostępniany na <a href="https://creativecommons.org/licenses/by-sa/3.0/deed.pl">licencji Creative Commons: uznanie autorstwa, na tych samych warunkach</a>, z możliwością obowiązywania dodatkowych ograniczeń.
Zobacz szczegółowe informacje o <a href="https://wikimediafoundation.org/wiki/Warunki_korzystania">warunkach korzystania</a></small></p>

<p><small><strong>Źródło</strong>: <a href="{url}">{url}</a></small></p>
    """

    # e.g. https://pl.wikipedia.org/wiki/Kirkja
    URL_RE = r'https?://([^/]+)/wiki/(.*)$'

    def set_up(self):
        self._url = self.extend_url(self._url)

    @staticmethod
    def extend_url(url):
        # https://pl.wikipedia.org/wiki/Kirkja
        # https://pl.wikipedia.org/w/index.php?title=Kirkja&printable=yes
        matches = re.match(WikipediaSource.URL_RE, url)

        return 'https://{domain}/w/index.php?title={title}&printable=yes'.format(
            domain=matches.group(1), title=matches.group(2)) if matches else None

    @staticmethod
    def is_my_url(url):
        return re.match(WikipediaSource.URL_RE, url) is not None

    def get_html(self):
        article = self.xpath('//*[@id="mw-content-text"]')

        # clean up the HTML
        xpaths = [
            'div[div[@class="thumbinner"]]',  # images
            'div[@class="toc"]',  # TOC
            'table',  # infobox
            '*//div[contains(@class, "noprint")]',  # non printable content
            '*//span[@class="mw-editsection"]',  # edit sections
        ]
        article = self.remove_nodes(article, xpaths)

        html = self.get_node_html(article)

        # remove internal links
        # <a href="/wiki/Klif" title="Klif">wybrzeża klifowe</a>
        def link_replace(match):
            content = match.group(1)  # e.g. [1]
            is_ref = re.match(r'\[\d+\]', content)

            return match.group(0) if is_ref else content

        html = re.sub(r'<a[^>]*>([^<]+)</a>', link_replace, html)

        # add a title and a footer
        return '\n'.join([
            self.HEADER.format(title=self.get_title(), author=self.get_author()).strip(),
            html,
            self.FOOTER.format(url=self._url).strip()
        ])

    def get_title(self):
        return self.get_node('//h1').strip()

    def get_author(self):
        return self.get_node('//*[@id="siteSub"]')

    def get_language(self):
        return self.get_node('//h1', 'lang')
