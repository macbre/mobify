"""mobify

Download a web page (set of web pages) as an e-book.

Usage:
  mobify URL ...
  mobify (-h | --help)
  mobify --version

Options:
  URL           Space-separated list of URLs to fetch.
  -h --help     Show this screen.
  --version     Show version.
"""

import logging
import subprocess

from docopt import docopt

from .errors import MobifyError
from .publisher import Publisher
from .version import version


def main():
    """ Main entry point for CLI"""
    logger = logging.getLogger(__name__)

    arguments = docopt(__doc__, version='mobify {}'.format(version))
    logger.debug('Options: {}'.format(arguments))

    chapters = arguments['URL']
    logger.info('URL:   {}'.format(chapters))

    try:
        publisher = Publisher(chapters=chapters)
        publisher.publish()

        # convert epub to mobi
        epub_file = publisher.get_dest()
        mobi_file = publisher.get_dest('mobi')
        logger.info('Converting to mobi: {}'.format(mobi_file))

        subprocess.call(['ebook-convert', epub_file, mobi_file], stderr=subprocess.STDOUT)

        logger.info('Converting completed')

    except MobifyError as ex:
        logger.error('Failed to generate an ebook', exc_info=True)

        print(ex)
        exit(2)
