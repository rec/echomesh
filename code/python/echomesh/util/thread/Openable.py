from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Log

LOGGER = Log.logger(__name__)

class Openable(object):
  def __init__(self, parent=None):
    self.is_open = True
    self.set_parent(parent)

  def set_parent(self, parent):
    self.parent = parent

  def start(self):
    LOGGER.debug('Starting %s', self)

  def close(self):
    if self.is_open:
      LOGGER.debug('Closing %s', self)
      self.is_open = False
      if self.parent:
        LOGGER.debug('Closing parent %s', self.parent)
        self.parent and self.parent.close()

  def join(self):
    LOGGER.debug('Joining %s', self)

  def __enter__(self):
    return self

  def __exit__(self, type, value, traceback):
    self.close()
