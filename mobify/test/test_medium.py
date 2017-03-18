# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from . import MobifyTestCase
from mobify.sources import MediumSource


class MediumSourceTest(MobifyTestCase):

    _source = None

    def setUp(self):
        self._source = MediumSource(
            url=str('https://medium.com/javascript-scene/assessing-employee-performance-1a8bdee45c1a'),
            content=self.get_fixture('medium.html')
        )

    @staticmethod
    def test_is_my_url():
        assert MediumSource.is_my_url('https://medium.com/javascript-scene/assessing-employee-performance')
        assert not MediumSource.is_my_url('http://pl.wikipedia.pl/wiki/Foo')


    def test_parsing(self):
        assert self._source.get_title() == 'Assessing Employee Performance'
        assert self._source.get_author() == 'Eric Elliott'
        assert self._source.get_language() == 'en'

        html = self._source.get_html()
        print(html)  # failed assert will print the raw HTML

        assert '<h2>You’re Doing it Rong</h2>' in html
        assert'<blockquote>Your people make such a big impact,<br>you can’t afford to take shortcuts.</blockquote>' \
              in html
        assert '<img' not in html, "TOC should be removed"
