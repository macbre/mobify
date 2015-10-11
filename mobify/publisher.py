import logging

from ebooklib import epub

from .source import MobifySource

class Publisher(object):
    def __init__(self, url=None, chapters=None):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.info('Creating en epub for <{}>'.format(url))

        if url is not None:
            self._chapters = [url]
        elif chapters is not None:
            self._chapters = chapters
        else:
            raise AttributeError('url or chapters must be provided')

    def add_chapter(self, url):
        self._logger.info('Adding a chapter <{}>'.format(url))
        self._chapters.append(url)

    def publish(self, dest):
        sources = [MobifySource.find_source_for_url(url) for url in self._chapters]

        # @see https://github.com/booktype/ebooklib/blob/master/samples/03_advanced_create/create.py
        book = epub.EpubBook()

        # add metadata
        source = sources[0]
        book.set_title(source.get_title())
        book.add_author(source.get_author())
        book.set_language(source.get_language())

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

            self._logger.info('Chapter #{}: {}'.format(chapter_id, chapter.title.encode('utf8')))
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
        self._logger.info('Publising epub')

        epub.write_epub(dest, book, {})

        self._logger.info('Publising epub completed')
        return True
