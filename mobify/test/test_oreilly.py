# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from . import MobifyTestCase
from mobify.sources import OReillySource


class OReillySourceTest(MobifyTestCase):

    _source = None

    def setUp(self):
        self._source = OReillySource(
            url=str('https://www.oreilly.com/ideas/the-evolution-of-devops'),
            content=self.get_fixture('oreilly.html')
        )

    @staticmethod
    def test_is_my_url():
        assert OReillySource.is_my_url('https://www.oreilly.com/ideas/the-evolution-of-devops')
        assert not OReillySource.is_my_url('https://www.oreilly.com/topics/operations')

    def test_parsing(self):
        assert self._source.get_title() == 'The evolution of DevOps'
        assert self._source.get_author() == 'Mike Loukides'
        assert self._source.get_language() == 'en'

        html = self._source.get_html()
        print(html)  # failed assert will print the raw HTML

        assert '<p>A few years ago, I wrote that DevOps is ' in html
        assert '<h2>Automation and operations at scale</h2>' in html

        assert 'Black and White (source:' not in html, "Images should be removed"
        assert "O'Reilly Velocity Conference in New York, Oct. 1-4, 2017" not in html, "Ads should be removed"
