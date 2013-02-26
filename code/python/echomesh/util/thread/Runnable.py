from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Log

LOGGER = Log.logger(__name__)

class Runnable(object):
  STOP, PAUSE, RUN = range(3)

  def __init__(self):
    self.is_running = Runnable.STOP

  def run(self):
    if not self.is_running:
      self.is_running = Runnable.RUN
      self._on_run()
      LOGGER.debug('Started %s', self)

  def stop(self):
    if self.is_running:
      self.is_running = Runnable.STOP
      self._on_stop()
      LOGGER.debug('Stopped %s', self)

  def _on_stop(self):
    pass

  def _on_run(self):
    pass

  def __enter__(self):
    return self

  def __exit__(self, type, value, traceback):
    self.stop()
