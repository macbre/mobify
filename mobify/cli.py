import logging
import subprocess

from .publisher import Publisher

def main():
    """ Main entry point for CLI"""
    # TODO: handle getopt

    logger = logging.getLogger(__name__)

    chapters = [
        'http://histmag.org/czy-brytyjczycy-zdradzili-polskich-lotnikow-slow-kilka-o-polskiej-wojennej-mitologii-11972;0',
        'http://histmag.org/polacy-w-bitwie-o-anglie-czas-o-nich-przypomniec-11897'
    ]

    """
    chapters = [
        'http://histmag.org/Niech-zyje-Car-Wladyslaw-Zygmuntowicz-Cz.-1-Rachuby-polityczne-i-wybuch-wojny-8350;0',
        'http://histmag.org/Niech-zyje-car-Wladyslaw-Zygmuntowicz-Cz.-2-Hetman-Stanislaw-Zolkiewski-w-rokowaniach-z-Moskwa-8386;0',
        'http://histmag.org/Niech-zyje-car-Wladyslaw-Zygmuntowicz-Cz.-3-Upadek-planow-hetmana-8449;0'
    ]
    """

    logger.info('URL:   {}'.format(chapters))

    publisher = Publisher(chapters=chapters)
    publisher.publish()

    # convert epub to mobi
    epub_file = publisher.get_dest()
    mobi_file = epub_file.replace('.epub', '.mobi')
    logger.info('Converting to mobi: {}'.format(mobi_file))

    subprocess.call(['ebook-convert', epub_file, mobi_file], stderr=subprocess.STDOUT)

    logger.info('Converting completed')
