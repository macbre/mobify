# -*- coding: utf-8 -*-
from __future__ import print_function

from . import MobifyTestCase
from mobify.sources.histmag import HistmagPage, HistmagSource


class Histmag(MobifyTestCase):

    @staticmethod
    def test_is_my_url():
        assert not HistmagSource.is_my_url('http://example.com')
        assert HistmagSource.is_my_url(
            'http://histmag.org/Niech-zyje-car-Wladyslaw-Zygmuntowicz-Cz.-3-Upadek-planow-hetmana-8449')
        assert HistmagSource.is_my_url(
            'https://histmag.org/czy-powstanie-listopadowe-bylo-skazane-na-porazke-13520')

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


class HistmagBeniowski(MobifyTestCase):

    _source = None

    def setUp(self):
        # @see https://histmag.org/Maurycy-Beniowski-bunt-na-Kamczatce-13947
        self._source = HistmagPage(
            url='',
            content=self.get_fixture('Maurycy-Beniowski-bunt-na-Kamczatce.html')
        )

    def test_parsing(self):
        assert self._source.get_title() == 'Maurycy Beniowski - bunt na Kamczatce'
        assert self._source.get_lead() == u'Po upadku konfederacji barskiej został zesłany na Kamczatkę. Awanturnicza natura nie pozwoliła mu jednak długo zagrzać tam miejsca. Tak Maurycy Beniowski stanął na czele buntu. Czy wywalczył upragnioną wolność?'
        assert self._source.get_author() == u'Mateusz Będkowski'
        assert self._source.get_language() == 'pl'

        html = self._source.get_html()
        print(html)  # failed assert will print the raw HTML

        assert '<h1>Maurycy Beniowski - bunt na Kamczatce</h1>' in html
        assert '<p><strong>Po upadku konfederacji barskiej' in html
        assert u'<p>W październiku 1769 roku Beniowski i Wynbladth uczestniczyć mieli w spisku' in html

        assert 'Kamczatka, ilustracja' not in html
        assert 'Maurycy Beniowski (1741-1786) (domena publiczna)' not in html
        assert u'<h4>Zobacz także:</h4>' not in html


class HistmagChurchill(MobifyTestCase):

    _source = None

    def setUp(self):
        # @see https://histmag.org/Winston-Churchill-lew-Albionu-14521
        self._source = HistmagPage(
            url='',
            content=self.get_fixture('Winston-Churchill-lew-Albionu-14521.html')
        )

    def test_parsing(self):
        assert self._source.get_title() == 'Winston Churchill – lew Albionu'
        assert self._source.get_lead() == ''
        assert self._source.get_author() == u'Michał Gadziński'
        assert self._source.get_language() == 'pl'

        html = self._source.get_html()
        print(html)  # failed assert will print the raw HTML

        assert '<h1>Winston Churchill – lew Albionu</h1>' in html
        assert '<h3>Potomek księcia Marlborough</h3>' in html
        assert '<p>Winston Leonard Spencer-Churchill przyszedł na świat 30 listopada 1874 roku. ' in html

        assert u'<h3>Tekst jest fragmentem e-booka Michała Gadzińskiego „Perły imperium brytyjskiego”:</h3>' not in html
