# -*- coding: utf-8 -*-
import json
import re

from mobify.source import MobifySource


class HistmagSource(MobifySource):
    HEADER = u"""
<h1>{title}</h1>
<p><strong>{lead}</strong></p>
<p><small>{author}</small><br></p>
    """

    FOOTER = u"""
<br><br>
<hr>
<p><small>Wolna licencja – ten materiał został opublikowany na licencji Creative Commons Uznanie autorstwa
Na tych samych warunkach 3.0 Polska.</small></p>

<p><small>Redakcja i autor zezwalają na jego dowolny przedruk i wykorzystanie (również w celach komercyjnych) pod
następującymi warunkami: należy wyraźnie wskazać autora materiału oraz miejsce pierwotnej publikacji –
Portal historyczny Histmag.org, a także nazwę licencji (CC BY-SA 3.0) wraz z odnośnikiem do jej postanowień.
W przypadku przedruku w internecie konieczne jest także zamieszczenie dokładnego aktywnego
odnośnika do materiału objętego licencją.</small></p>

<p><small><strong>Źródło</strong>: <a href="{url}">{url}</a></small></p>
    """

    @staticmethod
    def is_my_url(url):
        return '//histmag.org/' in url

    @staticmethod
    def extend_url(url):
        url = url.split('?')[0]
        return url

    def get_inner_html(self):
        # <div style="margin-top:-24px" id="article">
        article = self.xpath('//div[@id="article"]')

        # clean up the HTML
        xpaths = [
            '*//div[@class="py-0.5"]',  # zobacz też
            '*//div[contains(@class,"flex")]',  # reklama
            '*//div[contains(@style,"flex")]',  # reklama
            '*//div[@class="py-8"]',  # polecajki
            '*//*[@class="childrenblocks"]',  # ilustracje
            '*//iframe',  # youtube
        ]
        article = self.remove_nodes(article, xpaths)

        html = self.get_node_html(article)

        # tags cleanup
        html = re.sub(r'<h1[^>]+>[^>]+</h1>', '', html)
        html = re.sub(r'<h2></h2>', '', html)
        html = re.sub(r'<p>\s*</p>', '', html)
        html = re.sub(r'</?(span|a|img|em|div)[^>]*>', '', html)

        html = html.replace('zobacz też:', '')
        html = html.replace(self.get_lead(), '')

        return html

    def get_html(self):
        # add a title and a footer
        return '\n'.join([
            self.HEADER.format(title=self.get_title(), author=self.get_author(), lead=self.get_lead()).strip(),
            self.get_inner_html(),
            self.FOOTER.format(url=self._url).strip()
        ]).strip()

    def get_title(self):
        # <h1 style="...">Droga Leopolda II do własnej kolonii. Jak król Belgii stworzył w Afryce system zagłady?</h1>
        return self.get_node('//h1').strip()

    def _get_metadata(self) -> dict:
        # <script type="application/ld+json">
        meta = self.get_node('//script[@type="application/ld+json"]')
        try:
            # "@type": "Article",
            # "headline": "Droga Leopolda II do własnej kolonii. Jak król Belgii stworzył w Afryce system zagłady?",
            # "image": "https://histmag.org/grafika/2020_articles/LeopoldII/6_leopold.jpg  ",
            #  "author": "Paweł Marcinkiewicz",
            #  "description": "W latach 1885-1908, w Wolnym Państwie Kongo, ..."
            data = json.loads(meta)

            return data
        except:
            return {}

    def get_lead(self):
        lead = self._get_metadata().get('description', '')

        return lead.strip() if lead else ''

    def get_author(self):
        return self._get_metadata().get('author', '')

    def get_language(self):
        return 'pl'
