# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from . import MobifyTestCase
from mobify.sources import LocalFoSource


class LocalFoSourceTest(MobifyTestCase):

    _source = None

    def setUp(self):
        self._source = LocalFoSource(
            url=str('http://local.fo/change-indifference-active-stance-favour-pilot-whale-hunting/'),
            content=self.get_fixture('local_fo.html')
        )

    @staticmethod
    def test_is_my_url():
        assert LocalFoSource.is_my_url('http://local.fo/asked-make-cultural-sacrifice-states-dr-weihe-finds-problematic-health-faroese-eat-pilot-whales/')
        assert not LocalFoSource.is_my_url('http://pl.wikipedia.pl/wiki/Foo')

    def test_parsing(self):
        assert self._source.get_title() == 'The change from indifference to an active stance in favour of pilot whale hunting'
        assert self._source.get_author() == 'Local.fo'
        assert self._source.get_language() == 'en'

        html = self._source.get_html()
        print(html)  # failed assert will print the raw HTML

        assert '<h1>The change from indifference to an active stance in favour of pilot whale hunting</h1>' in html
        assert'<em>Originally published' in html
