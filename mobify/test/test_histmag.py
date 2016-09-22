# -*- coding: utf-8 -*-
from __future__ import print_function

from . import MobifyTestCase
from mobify.sources.histmag import HistmagChapter, HistmagSource


class Histmag(MobifyTestCase):

    _source = None

    def setUp(self):
        self._source = HistmagChapter(
            url='',
            content=self.get_fixture('Maurycy-Beniowski-bunt-na-Kamczatce.html')
        )

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

    def test_parsing(self):
        assert self._source.get_title() == 'Maurycy Beniowski - bunt na Kamczatce'
        assert self._source.get_lead() == u'Po upadku konfederacji barskiej został zesłany na Kamczatkę. Awanturnicza natura nie pozwoliła mu jednak długo zagrzać tam miejsca. Tak Maurycy Beniowski stanął na czele buntu. Czy wywalczył upragnioną wolność?'
        assert self._source.get_author() == u'Mateusz Będkowski'
        assert self._source.get_language() == 'pl'

        html = self._source.get_html()
        print(html)  # failed assert will print the raw HTML

        assert '<h1>Maurycy Beniowski - bunt na Kamczatce</h1>' in html
        assert u'<p><strong>Po upadku konfederacji barskiej został zesłany na Kamczatkę' in html
        assert u'<p>W październiku 1769 roku Beniowski i Wynbladth uczestniczyć mieli w spisku' in html

        assert 'Kamczatka, ilustracja' not in html
        assert 'Maurycy Beniowski (1741-1786) (domena publiczna)' not in html
        assert '<h4>Zobacz także:</h4>' not in html
