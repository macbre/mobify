import logging
from os import getenv

# import all sources
from .sources import HistmagSource

# setup the logger
is_dev = getenv('DEBUG', 0) == '1'

logging.basicConfig(
    level=logging.DEBUG if is_dev else logging.INFO,
    format='%(asctime)s %(name)-25s %(levelname)-8s %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S"
)
