from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import logging.config

logger = logging.getLogger('simpleExample')

fh = logging.FileHandler('/tmp/xxx/test.log')
logger.addHandler(fh)
logger.debug("debug message")
logger.info("info message")
logger.warn("warn message")
logger.error("error message")
logger.critical("critical message")
