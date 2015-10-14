import logging

from ebooklib import epub

from. errors import PublisherNoChaptersError
from .source import MobifySource

class Publisher(object):
    def __init__(self, url=None, chapters=None):
        self._logger = logging.getLogger(self.__class__.__name__)

        if url is not None:
            self._chapters = [url]
        elif chapters is not None:
            self._chapters = chapters
        else:
            raise AttributeError('url or chapters must be provided')

        self._logger.info('Creating an epub for {}'.format(self._chapters))
        self._dest = self.get_dest_from_chapters(self._chapters)

    def add_chapter(self, url):
        self._logger.info('Adding a chapter <{}>'.format(url))
        self._chapters.append(url)

    @staticmethod
    def get_dest_from_chapters(chapters):
        if chapters is None or len(chapters) < 1:
            return None

        chapter = chapters[0]

        dest = chapter.split('/').pop()
        return dest

    def get_dest(self, ext='epub'):
        """
        :rtype: str
        """
        return '{}.{}'.format(self._dest, ext)

    def publish(self):
        sources = [MobifySource.find_source_for_url(url) for url in self._chapters]
        sources = [source for source in sources if source]

        if len(sources) == 0:
            raise PublisherNoChaptersError('No chapters in the book')

        # @see https://github.com/booktype/ebooklib/blob/master/samples/03_advanced_create/create.py
        book = epub.EpubBook()

        # add metadata
        source = sources[0]
        book.set_title(source.get_title())
        book.add_author(source.get_author())
        book.set_language(source.get_language())

        self._logger.info('Book title: {}'.format(book.title.encode('utf8')))
        self._logger.info('Book metadata: {}'.format(book.metadata))

        # add chapter(s)
        self._logger.info('Preparing chapters')

        chapters = []
        chapter_id = 1

        for source in sources:
            chapter = epub.EpubHtml(
                title=source.get_title(),
                file_name='{}.xhtml'.format(chapter_id),
                content=source.get_html()
            )

            chapters.append(chapter)
            book.add_item(chapter)

            self._logger.info('Chapter #{}: "{}"'.format(chapter_id, chapter.title.encode('utf8')))
            chapter_id += 1

        self._logger.info('{} chapter(s) added'.format(len(chapters)))

        # prepare navigation
        if len(chapters) > 1:
            book.toc = chapters
            book.add_item(epub.EpubNcx())
            book.add_item(epub.EpubNav())

            # spines
            book.spine = ['nav'] + chapters
        else:
            book.spine = chapters

        # write
        self._logger.info('Publising epub to {}'.format(self.get_dest()))

        epub.write_epub(self.get_dest(), book, {})

        self._logger.info('Publising epub completed')
        return True
