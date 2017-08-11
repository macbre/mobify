# -*- coding: utf-8 -*-
import re

from mobify.source import MobifySource


class DziejePlSource(MobifySource):

    HEADER = u"""
<h1>{title}</h1>
<p><strong>{lead}</strong></p>
<p><small>{author}</small><br></p>
"""

    FOOTER = u"""
<br><br>
<hr>
<p><small>
Wszelkie materiały (w szczególności depesze agencyjne, zdjęcia, grafiki, filmy) zamieszczone w niniejszym
Portalu chronione są przepisami ustawy z dnia 4 lutego 1994 r. o prawie autorskim i prawach pokrewnych oraz ustawy
z dnia 27 lipca 2001 r. o ochronie baz danych. Materiały te mogą być wykorzystywane wyłącznie na postawie stosownych
umów licencyjnych. Jakiekolwiek ich wykorzystywanie przez użytkowników Portalu, poza przewidzianymi przez przepisy
prawa wyjątkami, w szczególności dozwolonym użytkiem osobistym, bez ważnej umowy licencyjnej jest zabronione.
</small></p>

<p><small><strong>Źródło</strong>: <a href="{url}">{url}</a></small></p>
    """

    @staticmethod
    def is_my_url(url):
        return '//dzieje.pl/' in url

    def get_inner_html(self):
        article = self.xpath('//*[@property="schema:text"]')

        # clean up the HTML
        xpaths = [
            'blockquote[p]'
        ]
        article = self.remove_nodes(article, xpaths)

        html = self.get_node_html(article)

        return html

    def get_html(self):
        # add a title and a footer
        return '\n'.join([
            self.HEADER.format(title=self.get_title(), author=self.get_author(), lead=self.get_lead()).strip(),
            self.get_inner_html(),
            self.FOOTER.format(url=self._url).strip()
        ]).strip()

    def get_title(self):
        # <meta property="og:title" content="Radio w Poznaniu rozpoczęło nadawanie 90 lat temu" />
        return self.get_node('//meta[@property="og:title"]', attr='content').strip()

    def get_lead(self):
        # <meta property="og:description" content="90 lat temu, 24 kwietnia 1927 roku nadawanie rozpoczęła..." />
        lead = self.get_node('//meta[@property="og:description"]', attr='content').strip()

        return lead.strip() if lead else ''

    def get_author(self):
        return 'dzieje.pl'

    def get_language(self):
        return 'pl'
