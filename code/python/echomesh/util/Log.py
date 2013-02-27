from __future__ import absolute_import, division, print_function, unicode_literals

"""Typical usage:  at the top of your file:

LOGGER = Log.logger(__name__)
"""

import logging
import logging.config
import sys
import traceback

VERBOSE_LOGGING = False
PRINT_STACK_TRACES = False
DEFAULT_FORMAT = '%(message)s'
DEBUG_FORMAT = '%(name)s: %(message)s'
FILE_FORMAT = '"%(asctime)s %(levelname)s: %(name)s: %(message)s'
DEBUG = False
STACK_TRACES = False
LOG_LEVEL = 'INFO'

from echomesh.util.file import MakeDirs

class ConfigSetter(object):
  def config_update(self, get):
    self.debug = DEBUG or (get and get('debug'))
    self.stack_traces = STACK_TRACES or self.debug or (
      get and get('diagnostics', 'stack_traces'))
    self.log_level = (get and get('logging','level').upper()) or LOG_LEVEL

    self.kwds = {u'level': getattr(logging, self.log_level)}
    f = get and get('logging', 'file')
    if f:
      self.kwds[u'filename'] = f
    else:
      self.kwds[u'stream'] = sys.stdout

    self.kwds[u'format'] = (get and get('logging', 'format')) or (
      FILE_FORMAT if f else
      DEBUG_FORMAT if self.debug
      else DEFAULT_FORMAT)

    logging.basicConfig(**self.kwds)


CONFIG = ConfigSetter()
try:
  from echomesh.base import Config
  Config.add_client(CONFIG)
except:
  CONFIG.config_update(None)

def _error_wrapper(error_logger):
  def f(message, *args, **kwds):
    exc_type, exc_value = sys.exc_info()[:2]
    if exc_type:
      message = '%s: %s' % (exc_value, message)
      kwds['exc_info'] = kwds.get('exc_info', CONFIG.stack_traces)
    error_logger(message, *args, **kwds)
  return f

def logger(name=None):
  log = logging.getLogger(name or 'logging')
  log.error = _error_wrapper(log.error)
  return log

LOGGER = logger(__name__)
LOGGER.debug('Log level is %s', CONFIG.log_level)

