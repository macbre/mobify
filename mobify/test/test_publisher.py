# -*- coding: utf-8 -*-
from unittest import TestCase
from mobify.publisher import Publisher


class PublisherTest(TestCase):

    @staticmethod
    def test_get_dest_from_chapters():
        assert Publisher.get_dest_from_chapters(None, 'mobi') is None
        assert Publisher.get_dest_from_chapters([], 'mobi') is None
        assert Publisher.get_dest_from_chapters(['foo'], 'mobi') == 'foo.mobi'
        assert Publisher.get_dest_from_chapters(['http://example.com/foo'], 'mobi') == 'foo.mobi'
        assert Publisher.get_dest_from_chapters(['http://example.com/foo/bar'], 'mobi') == 'bar.mobi'
        assert Publisher.get_dest_from_chapters(['http://example.com/foo/bar'], 'epub') == 'bar.epub'
