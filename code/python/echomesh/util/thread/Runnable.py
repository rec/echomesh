from __future__ import absolute_import, division, print_function, unicode_literals

import threading

from echomesh.util import Log

LOGGER = Log.logger(__name__)

class Runnable(object):
  def __init__(self):
    self.is_running = False
    self._lock = threading.RLock()

  def run(self):
    with self._lock:
      if not self.is_running:
        self.is_running = True
        self._on_run()
        LOGGER.debug('Started %s %s', self, self.is_running)
      else:
        LOGGER.debug('Tried to run a running %s', self)

  def stop(self):
    with self._lock:
      if self.is_running:
        self.is_running = False
        self._on_stop()
        LOGGER.debug('Stopped %s', self)
      else:
        LOGGER.debug('Tried to stop a stopped %s', self)

  def _on_stop(self):
    pass

  def _on_run(self):
    pass

  def __enter__(self):
    return self

  def __exit__(self, type, value, traceback):
    self.stop()
