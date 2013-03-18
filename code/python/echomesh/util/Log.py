"""Typical usage:  at the top of your file:

LOGGER = Log.logger(__name__)
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import logging.config
import sys
import traceback

DEBUG = False
STACK_TRACES = False

LOG_LEVEL = 'INFO'

DEFAULT_FORMAT = '%(message)s'
DEBUG_FORMAT = '%(message)s'
# DEBUG_FORMAT = '%(levelname)s: %(message)s'
FILE_FORMAT = '%(asctime)s %(levelname)s: %(name)s: %(message)s'

_LOG_SIGNATURE = 'util/Log.py'
_ERROR_COUNTER = {}

def _check_error_count(limit, every):
  for line in traceback.format_stack(): # reversed(traceback.format_stack()):
    if _LOG_SIGNATURE not in line:
      errors = _ERROR_COUNTER.get(line, 0)
      if limit is not None and errors >= limit * (every or 1):
        return False
      _ERROR_COUNTER[line] = errors + 1
      return not (every and (errors % every))


class ConfigSetter(object):
  def config_update(self, get):
    self.debug = DEBUG or (get and get('debug'))
    self.stack_traces = STACK_TRACES or self.debug or (
      get and get('diagnostics', 'stack_traces'))
    self.log_level = (get and get('logging','level').upper()) or LOG_LEVEL

    self.kwds = {u'level': getattr(logging, self.log_level)}
    self.filename = get and get('logging', 'file')
    if self.filename:
      self.kwds[u'filename'] = self.filename
    else:
      self.kwds[u'stream'] = sys.stdout

    self.kwds[u'format'] = (get and get('logging', 'format')) or (
      FILE_FORMAT if self.filename else
      DEBUG_FORMAT if self.debug
      else DEFAULT_FORMAT)

    logging.basicConfig(**self.kwds)


CONFIG = ConfigSetter()
try:
  from echomesh.base import Config
  Config.add_client(CONFIG)
except:
  CONFIG.config_update(None)


def logger(name=None):
  log = logging.getLogger(name or 'logging')
  original_error_logger = log.error

  def new_error_logger(*args, **kwds):
    limit = kwds.pop('limit', None)
    every = kwds.pop('every', None)

    if limit is not None or limit is not None:
      if not _check_error_count(limit, every):
        return

    message, args = (args[0] if args else ''), args[1:]
    exc_type, exc_value = sys.exc_info()[:2]
    if exc_type:
      message = '%s: %s' % (exc_value, message)
      kwds['exc_info'] = kwds.get('exc_info', CONFIG.stack_traces)
    if not CONFIG.filename:
      message = 'ERROR: %s' % message
    original_error_logger(message, *args, **kwds)

  log.error = new_error_logger
  return log


LOGGER = logger(__name__)
LOGGER.debug('Log level is %s', CONFIG.log_level)

