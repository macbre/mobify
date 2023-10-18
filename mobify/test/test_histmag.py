# -*- coding: utf-8 -*-
from __future__ import print_function

from . import MobifyTestCase
from mobify.sources.histmag import HistmagSource


class Histmag(MobifyTestCase):

    @staticmethod
    def test_is_my_url():
        assert not HistmagSource.is_my_url('http://example.com')
        assert HistmagSource.is_my_url(
            'http://histmag.org/Niech-zyje-car-Wladyslaw-Zygmuntowicz-Cz.-3-Upadek-planow-hetmana-8449')
        assert HistmagSource.is_my_url(
            'https://histmag.org/czy-powstanie-listopadowe-bylo-skazane-na-porazke-13520')
        assert HistmagSource.is_my_url(
            'https://histmag.org/Droga-Leopolda-II-do-wlasnej-kolonii.-Jak-krol-Belgii-stworzyl-w-Afryce-system-zaglady-21541')

    @staticmethod
    def test_extend_url():
        assert HistmagSource.extend_url(
            'http://histmag.org/Niech-zyje-car-Wladyslaw-Zygmuntowicz-Cz.-3-Upadek-planow-hetmana-8449'
        ) == 'http://histmag.org/Niech-zyje-car-Wladyslaw-Zygmuntowicz-Cz.-3-Upadek-planow-hetmana-8449'

        assert HistmagSource.extend_url(
            'http://histmag.org/Margaret-Thatcher-tajfun-reform-7896'
        ) == 'http://histmag.org/Margaret-Thatcher-tajfun-reform-7896'

        assert HistmagSource.extend_url(
            'http://histmag.org/zmarl-prof-janusz-tazbir-13257?newsletter=true'
        ) == 'http://histmag.org/zmarl-prof-janusz-tazbir-13257'

        assert HistmagSource.extend_url(
            'https://histmag.org/Prawdziwy-powod-wybuchu-I-wojny-swiatowej-9648?ciekawostka'
        ) == 'https://histmag.org/Prawdziwy-powod-wybuchu-I-wojny-swiatowej-9648'


class HistmagKoloniaBelgijska(MobifyTestCase):

    _source = None

    def setUp(self):
        # https://histmag.org/Droga-Leopolda-II-do-wlasnej-kolonii.-Jak-krol-Belgii-stworzyl-w-Afryce-system-zaglady-21541
        self._source = HistmagSource(
            url='',
            content=self.get_fixture('kolonia-belgijska.html')
        )

    def test_parsing(self):
        assert self._source.get_title() == 'Droga Leopolda II do własnej kolonii. Jak król Belgii stworzył w Afryce system zagłady?'
        assert self._source.get_lead().startswith('W latach 1885-1908, w Wolnym Państwie Kongo, zamordowano i okaleczono ponad')
        assert self._source.get_author() == 'Paweł Marcinkiewicz'
        assert self._source.get_language() == 'pl'

        html = self._source.get_html()
        print(html)  # failed assert will print the raw HTML

        assert '<h1>Droga Leopolda II do własnej kolonii. Jak król Belgii stworzył w Afryce system zagłady?</h1>' in html
        assert '<h2>Motywacje Leopolda</h2>' in html
        assert '<p>Leopold II rządził swoją kolonią przez dwadzieścia trzy lata.' in html

        assert 'Reklama' not in html
