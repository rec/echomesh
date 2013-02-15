from __future__ import absolute_import, division, print_function, unicode_literals

"""Typical usage:  at the top of your file:

LOGGER = Log.logger(__name__)
"""

import logging
import logging.config
import sys

from echomesh.util.file import MakeDirs

class ConfigSetter(object):
  def config_update(self, get):
    if get:
      self.kwds = {'format': get('logging', 'format')}
      f = get('logging', 'file')
      if f:
        self.kwds['filename'] = f

      self.log_level = get('logging','level').upper()

    else:
      self.kwds = {'format': '%(asctime)s %(levelname)s: %(name)s: %(message)s'}
      self.log_level = 'INFO'

    self.kwds['level'] = getattr(logging, self.log_level)
    if 'filename' not in self.kwds:
      self.kwds['stream'] = sys.stdout
    logging.basicConfig(**self.kwds)

CONFIG = ConfigSetter()
try:
  from echomesh.base import Config
  Config.add_client(CONFIG)
except:
  CONFIG.config_update(None)

def _print(string, *args):
  print(string % args)

def logger(name=None):
  log = logging.getLogger(name or 'logging')
  setattr(log, 'print', _print)
  return log

LOGGER = logger(__name__)
LOGGER.debug('Log level is %s', CONFIG.log_level)

