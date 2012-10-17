from __future__ import absolute_import, division, print_function, unicode_literals

"""Typical usage:  at the top of your file:

LOGGER = Log.logger(__name__)

"""

import logging
import logging.config

from config import Config
from util import MakeDirs

def _get_handler(config):
  lconf = config['logging']
  f = lconf.get('file', None)
  if f:
    MakeDirs.parent_makedirs(f)
    handler = logging.FileHandler(f)
    level = lconf.get('level', 'debug').upper()
    handler.setLevel(getattr(logging, level))
    return handler

HANDLER = _get_handler(Config.CONFIG)

def logger(name=None):
  log = logging.getLogger(name or 'logging')
  if HANDLER and HANDLER not in logging.handlers:
    log.addHandler(HANDLER)

  return log

