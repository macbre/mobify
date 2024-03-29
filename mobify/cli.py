"""mobify

Download a web page (set of web pages) as an e-book.

Usage:
  mobify URL ... [--source=<source>]
  mobify (-h | --help)
  mobify --version

Options:
  URL               Space-separated list of URLs to fetch.
  -h --help         Show this screen.
  --source=<source> Force a given source type
  --version         Show version.
"""

import logging

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
        publisher = Publisher(chapters=chapters, source_hint=arguments.get('--source'))
        publisher.publish()

        # store urls in the .mobify_history file
        with open('.mobify_history', 'a') as f:
            for url in chapters:
                f.write(url + '\n')

    except MobifyError as ex:
        logger.error('Failed to generate an ebook', exc_info=True)

        print(ex)
        exit(2)
