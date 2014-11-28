"""Typical usage:  at the top of your file, put:

LOGGER = Log.logger(__name__)
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import logging.config
import six
import sys
import traceback

FORCE_DEBUG = False
DINFO = 3.5
VDEBUG = 5

LOG_LEVEL = 'INFO'

DEFAULT_FORMAT = '%(message)s'
DEBUG_FORMAT = '%(asctime)s %(levelname)s: %(name)s: %(message)s'
FILE_FORMAT = '%(asctime)s %(levelname)s: %(name)s: %(message)s'

_LOG_SIGNATURE = 'util/Log.py'
_LOG_COUNTER = {}
_STREAM = None

def _suppress_this_line(limit, every):
    if limit is not None or every is not None:
        for line in traceback.format_stack():
            if _LOG_SIGNATURE not in line:
                count = _LOG_COUNTER.get(line, 0)
                if limit is not None and count >= limit * (every or 1):
                    return True
                _LOG_COUNTER[line] = count + 1
                return not (every and (count % every))

def _add_new_levels():
    logging.addLevelName(VDEBUG, 'VDEBUG')

    def vdebug(self, message, *args, **kws):
        self.log(VDEBUG, message, *args, **kws)

    logging.Logger.vdebug = vdebug
    logging.VDEBUG = VDEBUG

class _SettingsClient(object):
    def settings_update(self, get):
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

        if _STREAM:
            self.kwds[u'stream'] = _STREAM

        self.kwds = dict((str(k), v) for k, v in six.iteritems(self.kwds))
        logging.basicConfig(**self.kwds)

def _reconfigure():
    try:
        from echomesh.base import Settings
    except:
        _SETTINGS.settings_update(None)
    else:
        Settings.add_client(_SETTINGS)

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
            exc_info = False
            if exc_type:
                message = '%s %s' % (exc_value, message)
                exc_info = kwds.get('exc_info', _SETTINGS.stack_traces)
                kwds['exc_info'] = exc_info
            if not _SETTINGS.filename:
                message = 'ERROR: %s\n\n' % message
        original_logger(message, *args, **kwds)

    setattr(logger, name, new_logger)
    return new_logger

_SETTINGS = None

def _configure():
    global _SETTINGS, _LOGGER
    if not _SETTINGS:
        _add_new_levels()
        _SETTINGS = _SettingsClient()
        _reconfigure()
        _LOGGER = logger(__name__)
        _LOGGER.debug('\nLog level is %s', _SETTINGS.log_level)

_LOGGER_NAMES = 'vdebug', 'debug', 'error', 'warning', 'info'

class _Logger(object):
    def __init__(self, name):
        self._logger = None
        self._name = name

    def __getattr__(self, name):
        if name not in _LOGGER_NAMES:
            raise AttributeError(
                "'_Logger' object has no attribute '%s'" % name)

        _configure()
        if not self._logger:
            self._logger = logging.getLogger(self._name)
        attr = _make_logger(self._logger, name)
        setattr(self, name, attr)
        return attr

logger = _Logger

def set_stream(stream):
    """Set a stream to which all logging is redirected."""
    # Not used.
    assert hasattr(stream, 'write'), 'Streams need to have a write method'
    global _STREAM
    _STREAM = stream
    _reconfigure()
