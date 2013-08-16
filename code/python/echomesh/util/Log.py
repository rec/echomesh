"""Typical usage:  at the top of your file, put:

LOGGER = Log.logger(__name__)
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import logging.config
import six
import sys
import traceback

FORCE_DEBUG = not True
VDEBUG = 5

LOG_LEVEL = 'INFO'

DEFAULT_FORMAT = '%(message)s'
DEBUG_FORMAT = '%(asctime)s %(levelname)s: %(name)s: %(message)s'
FILE_FORMAT = '%(asctime)s %(levelname)s: %(name)s: %(message)s'

_LOG_SIGNATURE = 'util/Log.py'
_LOG_COUNTER = {}

def _suppress_this_line(limit, every):
  if limit is not None or every is not None:
    for line in traceback.format_stack():
      if _LOG_SIGNATURE not in line:
        count = _LOG_COUNTER.get(line, 0)
        if limit is not None and count >= limit * (every or 1):
          return True
        _LOG_COUNTER[line] = count + 1
        return not (every and (count % every))

def _add_level_vdebug():
  logging.addLevelName(VDEBUG, 'VDEBUG')

  def vdebug(self, message, *args, **kws):
    self.log(VDEBUG, message, *args, **kws)

  logging.Logger.vdebug = vdebug
  logging.VDEBUG = VDEBUG

_add_level_vdebug()

class _ConfigClient(object):
  def config_update(self, get):
    get = get or (lambda *x: None)
    self.debug = FORCE_DEBUG or get('debug')
    self.stack_traces = self.debug or get('diagnostics', 'stack_traces')
    self.log_level = (get('logging','level') or LOG_LEVEL).upper()
    if self.debug:
      if self.log_level not in ['DEBUG', 'VDEBUG']:
        self.log_level = 'DEBUG'

    self.kwds = {u'level': getattr(logging, self.log_level)}
    self.filename = get('logging', 'file')
    if self.filename:
      self.kwds[u'filename'] = self.filename
    else:
      self.kwds[u'stream'] = sys.stdout

    self.kwds[u'format'] = get('logging', 'format') or (
      FILE_FORMAT if self.filename else
      DEBUG_FORMAT if self.debug
      else DEFAULT_FORMAT)

    self.kwds = dict((str(k), v) for k, v in six.iteritems(self.kwds))
    logging.basicConfig(**self.kwds)


_CONFIG = _ConfigClient()
try:
  from echomesh.base import Config
except:
  _CONFIG.config_update(None)
else:
  Config.add_client(_CONFIG)


def _make_logger(logger, name):
  original_logger = getattr(logger, name)
  is_error = (name == 'error')

  def new_logger(*args, **kwds):
    limit = kwds.pop('limit', None)
    every = kwds.pop('every', None)
    raw = kwds.pop('raw', None)

    if not (limit is None and every is None):
      if _suppress_this_line(limit, every):
        return

    message, args = (args[0] if args else ''), args[1:]
    if is_error and not raw:
      exc_type, exc_value = sys.exc_info()[:2]
      if exc_type:
        message = '%s %s' % (exc_value, message)
        kwds['exc_info'] = kwds.get('exc_info', _CONFIG.stack_traces)
      if not _CONFIG.filename:
        message = 'ERROR: %s\n' % message
    original_logger(message, *args, **kwds)

  setattr(logger, name, new_logger)

def logger(name=None):
  assert name
  logger = logging.getLogger(name or 'echomesh')

  for name in 'vdebug', 'debug', 'error', 'warn', 'info':
    _make_logger(logger, name)
  return logger

LOGGER = logger(__name__)
LOGGER.debug('\nLog level is %s', _CONFIG.log_level)

