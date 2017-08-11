# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from . import MobifyTestCase
from mobify.sources import DziejePlSource


class DziejePlSourceTest(MobifyTestCase):

    _source = None

    def setUp(self):
        self._source = DziejePlSource(
            url=str('http://dzieje.pl/rozmaitosci/radio-w-poznaniu-rozpoczelo-nadawanie-90-lat-temu'),
            content=self.get_fixture('dzieje-pl.html')
        )

    @staticmethod
    def test_is_my_url():
        assert DziejePlSource.is_my_url('http://dzieje.pl/rozmaitosci/radio-w-poznaniu-rozpoczelo-nadawanie-90-lat-temu')
        assert not DziejePlSource.is_my_url('http://dzieje.net')

    def test_parsing(self):
        assert self._source.get_title() == 'Radio w Poznaniu rozpoczęło nadawanie 90 lat temu'
        assert self._source.get_author() == 'dzieje.pl'
        assert self._source.get_language() == 'pl'

        html = self._source.get_html()
        print(html)  # failed assert will print the raw HTML

        assert '<p>Pierwsza siedziba radia kierowanego przez Kazimierza Okoniewskiego ' in html
        assert '90 lat temu, 24 kwietnia 1927 roku nadawanie ' in html
        assert '<blockquote>' not in html, "Quotes should be removed"
