from __future__ import absolute_import, division, print_function, unicode_literals

"""Typical usage:  at the top of your file:

LOGGER = Log.logger(__name__)

"""

import logging
import logging.config
import sys

from config import Config
from util import MakeDirs

DEFAULT_LOG_FORMAT = '%(asctime)s %(levelname)s: %(name)s: %(message)s'
LOG_FORMAT = Config.CONFIG['logging'].get('format', DEFAULT_LOG_FORMAT)

DEFAULT_LOG_LEVEL = 'INFO'
LOG_LEVEL_STR = Config.CONFIG['logging'].get('level', DEFAULT_LOG_LEVEL).upper()
LOG_LEVEL = getattr(logging, LOG_LEVEL_STR)

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)


def _get_handler(config):
  lconf = config['logging']
  f = lconf.get('file', None)
  if f:
    MakeDirs.parent_makedirs(f)
    handler = logging.FileHandler(f)
    return handler

HANDLER = _get_handler(Config.CONFIG)

def logger(name=None):
  log = logging.getLogger(name or 'logging')
  if HANDLER and HANDLER not in log.handlers:
    log.addHandler(HANDLER)

  return log

