# -*- coding: utf-8 -*-


import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())

__doc__ = 'auto substitution for python type like modules, classes and functions (created by auxilium)'
__license__ = 'Apache License 2.0'

__author__ = 'sonntagsgesicht'
__email__ = 'sonntagsgesicht@icloud.com'
__url__ = 'https://github.com/sonntagsgesicht/sphinx-pytype-substitution'

__date__ = 'Monday, 04 October 2021'
__version__ = '0.1'
__dev_status__ = '3 - Alpha'  # '4 - Beta'  or '5 - Production/Stable'

__dependencies__ = ()
__dependency_links__ = ()
__data__ = ()
__scripts__ = ()

# this is just an example to demonstrate the auxilium workflow
# it can be removed safely

import sphinx


def setup(app=sphinx()):
    app.add_config_value('pytype_substitutions', None, False)
    app.add_config_value('buildins_substitutions', False, False, (bool,))
    return {'version': __version__, 'parallel_read_safe': True}