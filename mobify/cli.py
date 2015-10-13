import logging
import subprocess

from .publisher import Publisher

def main():
    """ Main entry point for CLI"""
    # TODO: handle getopt

    logger = logging.getLogger(__name__)

    chapters = [
        'http://histmag.org/Margaret-Thatcher-droga-do-premierostwa-7895',
        'http://histmag.org/Margaret-Thatcher-tajfun-reform-7896',
    ]

    #chapters = ['http://histmag.org/Wielkie-Ksiestwo-Poznanskie-nieudany-eksperyment-polskiej-autonomii-10643;0']

    logger.info('URL:   {}'.format(chapters))

    publisher = Publisher(chapters=chapters)
    publisher.publish()

    # convert epub to mobi
    epub_file = publisher.get_dest()
    mobi_file = publisher.get_dest('mobi')
    logger.info('Converting to mobi: {}'.format(mobi_file))

    subprocess.call(['ebook-convert', epub_file, mobi_file], stderr=subprocess.STDOUT)

    logger.info('Converting completed')
