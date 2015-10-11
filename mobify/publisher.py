import logging

from ebooklib import epub

from .source import MobifySource

class Publisher(object):
    def __init__(self, url):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.info('Creating en epub for <{}>'.format(url))

        self._url = url

    def publish(self, dest):
        source = MobifySource.find_source_for_url(self._url)

        # @see https://github.com/booktype/ebooklib/blob/master/samples/03_advanced_create/create.py
        book = epub.EpubBook()

        # add metadata
        book.set_title(source.get_title())
        book.add_author(source.get_author())
        book.set_language(source.get_language())

        # add chapter(s)
        self._logger.info('Preparing chapters')

        chapters = []
        chapter_id = 1

        chapter = epub.EpubHtml(
            title=source.get_title(),
            file_name='{}.xhtml'.format(chapter_id),
            content=source.get_html()
        )

        chapters.append(chapter)
        book.add_item(chapter)

        self._logger.info('Chapter #{}: {}'.format(chapter_id, chapter.title))

        self._logger.info('{} chapter(s) added'.format(len(chapters)))

        # prepare navigation
        book.toc = chapters
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        # spines
        book.spine = ['nav'] + chapters

        # write
        self._logger.info('Publising epub')

        epub.write_epub(dest, book, {})

        self._logger.info('Publising epub completed')
        return True
