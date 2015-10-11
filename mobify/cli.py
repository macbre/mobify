import logging

from .publisher import Publisher

def main():
    """ Main entry point for CLI"""
    logger = logging.getLogger(__name__)

    """
    url = 'http://histmag.org/zielona-wyspa-kazimierza-wielkiego-11848;0'
    ebook = 'zielona-wyspa-kazimierza-wielkiego.epub'

    logger.info('URL:   <{}>'.format(url))
    logger.info('Ebook: {}'.format(ebook))

    publisher = Publisher(url=url)
    """

    chapters = [
        'http://histmag.org/Niech-zyje-Car-Wladyslaw-Zygmuntowicz-Cz.-1-Rachuby-polityczne-i-wybuch-wojny-8350;0',
        'http://histmag.org/Niech-zyje-car-Wladyslaw-Zygmuntowicz-Cz.-2-Hetman-Stanislaw-Zolkiewski-w-rokowaniach-z-Moskwa-8386;0',
        'http://histmag.org/Niech-zyje-car-Wladyslaw-Zygmuntowicz-Cz.-3-Upadek-planow-hetmana-8449;0'
    ]
    ebook = 'Niech-zyje-car-Wladyslaw-Zygmuntowicz.epub'

    logger.info('URL:   {}'.format(chapters))
    logger.info('Ebook: {}'.format(ebook))

    publisher = Publisher(chapters=chapters)
    publisher.publish(ebook)
