import copy
import logging
import requests

from lxml import etree, html


class MobifySource(object):

    def __init__(self, url, content=None):
        """
        @type url str
        @type content str
        """
        self._http = requests.session()
        self._logger = logging.getLogger(self.__class__.__name__)

        self._url = url

        self._content = content if content is not None else None
        self._tree = None

        self.set_up()

    def set_up(self):
        pass

    @staticmethod
    def is_my_url(url):
        raise NotImplementedError

    def get_html(self):
        raise NotImplementedError

    def get_title(self):
        raise NotImplementedError

    def get_author(self):
        raise NotImplementedError

    def get_language(self):
        raise NotImplementedError

    def get_inner_html(self):
        """
        :rtype: str
        """
        return self.get_html()

    @property
    def content(self):
        """
        Lazy fetch the URL

        :rtype: str
        """
        if self._content is None:
            self._logger.info('Fetching <{}>'.format(self._url))

            resp = self._http.get(self._url)

            # @see http://docs.python-requests.org/en/master/api/#requests.Response
            resp.encoding = 'utf-8'  # force UTF-8
            self._content = resp.text

            self._logger.info('HTTP {}, got {:.2f} kB'.format(resp.status_code, 1.0 * len(self._content) / 1024))

            assert resp.status_code < 400, "Invalid HTTP response received"

        return self._content

    @property
    def tree(self):
        """
        Lazy HTML parsing

        :rtype: lxml.html.HtmlElement
        """
        if self._tree is None:
            self._logger.info('Parsing the content')
            self._tree = html.fromstring(self.content, base_url=self._url)

        return self._tree

    def xpath(self, xpath):
        """
        Get all nodes matching given XPath

        :rtype: lxml.html.HtmlElement
        """
        nodes = self.tree.xpath(xpath)
        return nodes[0] if len(nodes) > 0 else None

    def get_node(self, xpath, attr=None):
        """
        Get node's text content or attribute value using xpath

        :rtype: str
        """
        node = self.xpath(xpath)

        if node is not None:
            if attr is None:
                try:
                    return node.text
                except AttributeError:
                    # handle lxml.etree._ElementUnicodeResult - xpath with "text()'
                    return str(node)
            else:
                return node.attrib.get(attr)

        return None

    @staticmethod
    def get_node_html(node):
        """
        Get's the HTML content of a given node

        :rtype: str
        """
        return etree.tostring(node, pretty_print=True, method="html", encoding='utf8').decode('utf8')

    @staticmethod
    def remove_nodes(tree, xpaths):
        """
        Remove all sub nodes matching given XPath(s)

        :rtype: lxml.html.HtmlElement
        """
        tree = copy.copy(tree)

        for xpath in xpaths:
            nodes = tree.xpath(xpath)
            [node.getparent().remove(node) for node in nodes]

        return tree

    @classmethod
    def find_source_for_url(cls, url):
        """
        :rtype: MobifySource
        """
        logger = logging.getLogger(__name__)

        # get all subclasses of Source and MultiChapterSource
        sources = MobifySource.__subclasses__() + \
            MultiChapterSource.__subclasses__() + \
            MultiPageSource.__subclasses__()

        logger.info('Mobify sources defined: {}'.format(len(sources)))

        # check matching sources (via URL)
        for source in sources:
            logger.info('Checking "{}" source...'.format(source))

            try:
                if source.is_my_url(url) is True:
                    return source(url)
            # Abstract sources throw 'Exception: Not implemented'
            except NotImplementedError:
                pass

        logger.error('No source found for <{}>'.format(url))
        return None

    def __str__(self):
        return '<{} {}>'.format(self.__class__.__name__, self._url)


class MultiChapterSource(MobifySource):
    """
    Extend this class if you want to build a source that will return sources for sub-pages
    """
    def get_chapters(self):
        raise NotImplementedError

    @staticmethod
    def is_my_url(url):
        raise NotImplementedError

    def get_html(self):
        raise TypeError

    def get_title(self):
        raise TypeError

    def get_author(self):
        raise TypeError

    def get_language(self):
        raise TypeError


class MultiPageSource(MobifySource):
    """
    Extend this class if you want to build a source that will return sources for sub-pages,
    but will not created separate chapters
    """
    def get_pages(self):
        raise NotImplementedError

    @staticmethod
    def is_my_url(url):
        raise NotImplementedError

    def get_html(self):
        raise TypeError

    def get_title(self):
        raise TypeError

    def get_author(self):
        raise TypeError

    def get_language(self):
        raise TypeError
