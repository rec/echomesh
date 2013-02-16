from __future__ import absolute_import, division, print_function, unicode_literals

"""Typical usage:  at the top of your file:

LOGGER = Log.logger(__name__)
"""

import logging
import logging.config
import sys

VERBOSE_LOGGING = not True

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
    # logging.basicConfig(**self.kwds)
    logging.basicConfig(**dict((str(k), v) for (k, v) in self.kwds.iteritems()))

CONFIG = ConfigSetter()
try:
  from echomesh.base import Config
  Config.add_client(CONFIG)
except:
  CONFIG.config_update(None)

def _print(string, *args):
  print(string % args)

def _print_error(string, *args, **kwds):
  if kwds.get('exc_info'):
    print(sys.exc_info()[1])
  print('ERROR:', string % args)

def logger(name=None):
  log = logging.getLogger(name or 'logging')
  setattr(log, 'print', log.info if VERBOSE_LOGGING else _print)
  setattr(log, 'print_error', log.error if VERBOSE_LOGGING else _print_error)
  return log

LOGGER = logger(__name__)
LOGGER.debug('Log level is %s', CONFIG.log_level)

