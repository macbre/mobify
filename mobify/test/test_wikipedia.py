# -*- coding: utf-8 -*-
from . import MobifyTestCase
from mobify.sources import WikipediaSource


class WikipediaSourceTest(MobifyTestCase):

    _source = None

    def setUp(self):
        self._source = WikipediaSource(
            url='',
            content=self.get_fixture('wikipedia.html')
        )

    @staticmethod
    def test_is_my_url():
        assert not WikipediaSource.is_my_url('http://example.com')

        assert not WikipediaSource.is_my_url(
            'https://pl.wikipedia.org/w/index.php?title=Religia_S%C5%82owian&printable=yes')

        assert WikipediaSource.is_my_url('http://pl.wikipedia.pl/wiki/Foo')
        assert WikipediaSource.is_my_url('http://pl.wikipedia.pl/wiki/Foo/Bar')

        assert WikipediaSource.is_my_url('http://no.wikipedia.pl/wiki/Foo')

    @staticmethod
    def test_extend_url():
        assert WikipediaSource.extend_url(
            'https://pl.wikipedia.org/wiki/Religia_S%C5%82owian'
        ) == 'https://pl.wikipedia.org/w/index.php?title=Religia_S%C5%82owian&printable=yes'

        assert WikipediaSource.extend_url(
            'http://pl.wikipedia.pl/wiki/Foo %26 Bar'
        ) == 'https://pl.wikipedia.pl/w/index.php?title=Foo %26 Bar&printable=yes'

    def test_parsing(self):
        assert self._source.get_title() == 'Streymoy'
        assert self._source.get_author() == 'Z Wikipedii, wolnej encyklopedii'
        assert self._source.get_language() == 'pl'

        html = self._source.get_html()
        print(html)  # failed assert will print the raw HTML

        assert '<h1>Streymoy</h1>' in html
        assert u'<b>Streymoy</b> (duń. <i>Strømø</i>)' in html, "Basic HTML formatting should be kept"

        assert '<a href="#cite_note-Statystyki-1">[1]</a></sup>' in html, 'References should be kept'
        assert '<li id="cite_note-Statystyki-1">' in html, 'References should be kept'

        assert u'<h2>Spis treści</h2>' not in html, "TOC should be removed"
        assert 'edytuj kod' not in html, "Edit section should be removed"
        assert 'Kategoria' not in html, "Categories should be removed"
        assert 'Akwen' not in html, "Infobox should be removed"
        assert u'Osobny artykuł:' not in html, "Non printable content should be removed"
        assert u' title="Klif">wybrzeża klifowe</a>' not in html, "Internal links should be removed"
