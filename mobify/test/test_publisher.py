# -*- coding: utf-8 -*-
from unittest import TestCase
from mobify.publisher import Publisher


class PublisherTest(TestCase):

    @staticmethod
    def test_get_dest_from_chapters():
        assert Publisher.get_dest_from_chapters(None) is None
        assert Publisher.get_dest_from_chapters([]) is None
        assert Publisher.get_dest_from_chapters(['foo']) == 'foo'
        assert Publisher.get_dest_from_chapters(['http://example.com/foo']) == 'foo'
        assert Publisher.get_dest_from_chapters(['http://example.com/foo/bar']) == 'bar'
        assert Publisher.get_dest_from_chapters(
            ['https://pl.wikipedia.org/wiki/Religia_S%C5%82owian']) == 'Religia_S_C5_82owian'
