import logging

from .publisher import Publisher

def main():
    """ Main entry point for CLI"""
    logger = logging.getLogger(__name__)

    url = 'http://histmag.org/zielona-wyspa-kazimierza-wielkiego-11848;0'
    ebook = 'zielona-wyspa-kazimierza-wielkiego.epub'

    logger.info('URL:   <{}>'.format(url))
    logger.info('Ebook: {}'.format(ebook))

    publisher = Publisher(url)
    publisher.publish(ebook)
