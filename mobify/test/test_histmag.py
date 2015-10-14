# -*- coding: utf-8 -*-
from . import MobifyTestCase
from mobify.sources import HistmagSource


class Histmag(MobifyTestCase):

    _source = None

    def setUp(self):
        self._source = HistmagSource(
            url='',
            content=self.get_fixture('histmag-zielona-wyspa-kazimierza-wielkiego.html')
        )

    @staticmethod
    def test_is_my_url():
        assert not HistmagSource.is_my_url('http://example.com')
        assert HistmagSource.is_my_url(
            'http://histmag.org/Niech-zyje-car-Wladyslaw-Zygmuntowicz-Cz.-3-Upadek-planow-hetmana-8449;0')

    @staticmethod
    def test_extend_url():
        assert HistmagSource.extend_url(
            'http://histmag.org/Niech-zyje-car-Wladyslaw-Zygmuntowicz-Cz.-3-Upadek-planow-hetmana-8449;0'
        ) == 'http://histmag.org/Niech-zyje-car-Wladyslaw-Zygmuntowicz-Cz.-3-Upadek-planow-hetmana-8449;0'

        assert HistmagSource.extend_url(
            'http://histmag.org/Margaret-Thatcher-tajfun-reform-7896'
        ) == 'http://histmag.org/Margaret-Thatcher-tajfun-reform-7896;0'

    def test_parsing(self):
        assert self._source.get_title() == 'Zielona wyspa Kazimierza Wielkiego'
        assert self._source.get_author() == u'Marcin Sałański'
        assert self._source.get_language() == 'pl'

        html = self._source.get_html()
        print(html)  # failed assert will print the raw HTML

        assert '<h1>Zielona wyspa Kazimierza Wielkiego</h1>' in html
        assert '<h3>Z pustego i Salomon nie naleje</h3>' in html
        assert u'<p>Drugim istotnym źródłem królewskich dochodów był nowy system podatkowy.' in html

        assert '<p>Zielona wyspa Kazimierza Wielkiego</p>' not in html
        assert '<div id="article">' not in html
        assert '</div>' not in html
