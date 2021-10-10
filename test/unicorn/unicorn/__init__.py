# -*- coding: utf-8 -*-


import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())

__doc__ = 'always be a unicorn'
__license__ = 'Apache License 2.0'

__author__ = 'sonntagsgesicht'
__email__ = 'sonntagsgesicht@icloud.com'
__url__ = 'https://github.com/sonntagsgesicht/unicorn'

__date__ = 'Monday, 04 October 2021'
__version__ = '0.1'
__dev_status__ = '3 - Alpha'  # '4 - Beta'  or '5 - Production/Stable'

__dependencies__ = ()
__dependency_links__ = ()
__data__ = ()
__scripts__ = ()
__theme__ = ''

from .classes import *  # noqa
from .functions import *  # noqa
from .variables import *  # noqa
