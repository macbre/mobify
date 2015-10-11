# import all sources
from mobify.sources import HistmagSource

# setup the logger
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(name)-25s %(levelname)-8s %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S"
)

# version
__version__ = '0.1.0'
