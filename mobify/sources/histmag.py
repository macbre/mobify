# -*- coding: utf-8 -*-
import json
import re

from mobify.source import MultiPageSource, MobifySource


class HistmagSource(MultiPageSource):
    @staticmethod
    def is_my_url(url):
        return '//histmag.org/' in url

    @staticmethod
    def extend_url(url):
        url = url.split('?')[0]
        return url

    def get_pages(self):
        url = self.extend_url(self._url)

        # https://histmag.org/Droga-Leopolda-II-do-wlasnej-kolonii.-Jak-krol-Belgii-stworzyl-w-Afryce-system-zaglady-21541
        try:
            last_page_link = self.tree.xpath('//div[@class="paginator"][1]//a')[-1].attrib.get('href')
            last_page_no = int(last_page_link.split('/')[-1])  # 3
        except IndexError:
            last_page_no = 1

        pages = ['{}/{}'.format(url, page) for page in range(1, last_page_no+1)]

        self._logger.info('Chapters: {}'.format(pages))

        return [HistmagPage(url=page) for page in pages]


class HistmagPage(MobifySource):

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
        """
        This source cannot be created directly from Publisher
        """
        raise NotImplementedError

    def get_inner_html(self):
        article = self.xpath('//div[@id="styledcontent"]')

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
        html = re.sub(r'<h2></h2>', '', html)
        html = re.sub(r'<p>\s*</p>', '', html)
        html = re.sub(r'</?(span|a|img|em|div)[^>]*>', '', html)

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
        # <script id="__NEXT_DATA__" type="application/json">
        meta = self.get_node('//script[@id="__NEXT_DATA__"]')
        try:
            # {"props":{"pageProps":{"post":{"id":21541,"title":"D", "excerpt":"W
            data = json.loads(meta)

            return data['props']['pageProps']['post']
        except:
            return {}

    def get_lead(self):
        lead = self._get_metadata().get('excerpt', '')

        return lead.strip() if lead else ''

    def get_author(self):
        # <a style="text-decoration:none" href="#authors">Paweł Marcinkiewicz</a>
        return self.get_node('//a[@href="#authors"]').strip()

    def get_language(self):
        return 'pl'
