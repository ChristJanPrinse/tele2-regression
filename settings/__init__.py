import sys
import logging

from settings.input import *
from settings.profiles import *
from settings.base import *


try:
    from settings.local import *
except ImportError:
    logging.basicConfig(level=logging.WARNING, stream=sys.stderr)
