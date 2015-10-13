import logging
import subprocess

from .publisher import Publisher

def main():
    """ Main entry point for CLI"""
    # TODO: handle getopt

    logger = logging.getLogger(__name__)

    chapters = [
        'http://histmag.org/Wikingowie-i-poczatki-ich-wypraw-w-VIII-IX-w.-prawda-i-mity-8767',
        'http://histmag.org/Rola-smoka-w-mitologii-nordyckiej-4629',
        'http://histmag.org/Swen-Widlobrody-dunski-mocarz-8900',
        'http://histmag.org/Imie-krola-Haakona-czyli-jak-Norwegia-odzyskala-niepodleglosc-6098'
    ]

    chapters = ['http://histmag.org/Wielkie-Ksiestwo-Poznanskie-nieudany-eksperyment-polskiej-autonomii-10643;0']

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
