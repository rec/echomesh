from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Log

LOGGER = Log.logger(__name__)

class Runnable(object):
  def __init__(self):
    self.is_running = False

  def start(self):
    self.is_running = True
    LOGGER.debug('Starting %s', self)

  def stop(self):
    if self.is_running:
      LOGGER.debug('Closing %s', self)
      self.is_running = False

  def join(self):
    LOGGER.debug('Joining %s', self)

  def __enter__(self):
    return self

  def __exit__(self, type, value, traceback):
    self.stop()
