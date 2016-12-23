# -*- coding: utf-8 -*-
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

        # https://histmag.org/Maurycy-Beniowski-bunt-na-Kamczatce-13947/3
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
        article = self.xpath('//*[@class="middle"]')

        # clean up the HTML
        xpaths = [
            'table',
            'div[@class="paginator"]',
            'h4',  # Zobacz także
            '*//span/a[img]',  # big pictures
            '*//span/img',  # inline pictures
            'img',
            'div[@class="snippet"]',  # reklamy
            'h3[contains(text(), "Tekst jest fragmentem")]',  # fragmenty książek
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
        # <h1 class="title"><p>Maurycy Beniowski - bunt na Kamczatce</p></h1>
        return self.get_node('//div[contains(@class, "article_panel")]//p[1]').strip()

    def get_lead(self):
        # <h3 class="lead"><p>Po upadku konfederacji ...</p></h3>
        lead = self.get_node('//div[contains(@class, "article_panel")]//p[2]')

        return lead.strip() if lead else ''

    def get_author(self):
        return self.get_node('//*[contains(@class, "author_name")]//a/text()[2]').strip()

    def get_language(self):
        return 'pl'
