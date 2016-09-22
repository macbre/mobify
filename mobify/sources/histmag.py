# -*- coding: utf-8 -*-
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

    def set_up(self):
        self._url = self.extend_url(self._url)

        self._logger.info('Setting a referer...')
        self._http.headers['Referer'] = 'histmag.org/hello-from-mobify'

    @staticmethod
    def extend_url(url):
        url = url.split('?')[0]

        # extend the histmag.org URL to make it a single page article
        # http://histmag.org/Margaret-Thatcher-tajfun-reform-7896;0
        if not url.endswith(';0'):
            url += ';0'

        return url

    @staticmethod
    def is_my_url(url):
        return '//histmag.org/' in url

    def get_html(self):
        article = self.xpath('//*[@class="middle"]')

        # clean up the HTML
        xpaths = [
            'table',
            'div[@class="paginator"]',
            'h4',  # Zobacz także
            'p/span[img]',  # inline pictures
            'p/span[a/img]',  # big pictures
            'div[@class="snippet"]',  # reklamy
        ]
        article = self.remove_nodes(article, xpaths)

        html = self.get_node_html(article)

        # tags cleanup
        html = re.sub(r'<h2></h2>', '', html)
        html = re.sub(r'<p>\s*</p>', '', html)
        html = re.sub(r'</?(span|a|img|em|div)[^>]*>', '', html)

        # add a title and a footer
        return '\n'.join([
            self.HEADER.format(title=self.get_title(), author=self.get_author(), lead=self.get_lead()).strip(),
            html,
            self.FOOTER.format(url=self._url).strip()
        ])

    def get_title(self):
        # <h1 class="title"><p>Maurycy Beniowski - bunt na Kamczatce</p></h1>
        return self.get_node('//div[contains(@class, "article_panel")]//p[1]').strip()

    def get_lead(self):
        # <h3 class="lead"><p>Po upadku konfederacji ...</p></h3>
        return self.get_node('//div[contains(@class, "article_panel")]//p[2]').strip()

    def get_author(self):
        # <div class="author_name">Autor: <a href="https://histmag.org/profil/18785">Mateusz Będkowski </a><br>
        return self.get_node('//*[@class="author_name"]/a').strip()

    def get_language(self):
        return 'pl'
