from __future__ import absolute_import, division, print_function, unicode_literals

import weakref

from echomesh.util import Log
from echomesh.util import Openable

LOGGER = Log.logger(__name__)

class Closer(Openable.Openable):
  def __init__(self, *closers):
    super(Closer, self).__init__()
    try:
      self.closers = weakref.WeakSet(closers)
    except:
      self.closers = set()  # TODO: make sure this works in 2.6

  def start_all(self):
    for closer in self.closers:
      closer.start()

  def add_closer(self, *closers):
    self.closers.update(closers)

  def mutual_closer(self, *closers):
    for closer in closers:
      self.add_closer(closer)
      closer.add_closer(self)

  def close_all(self):
    for c in list(self.closers):
      try:
        if c and c.is_open:
          c.close()
      except:
        LOGGER.error("Couldn't close %s" % repr(c))
    self.closers.clear()

  def close(self):
    super(Closer, self).close()
    self.close_all()

  def join_all(self):
    for c in list(self.closers):
      try:
        c.join()
      except:
        pass

EXIT_CLOSER = Closer()

def close_on_exit(to_close):
  EXIT_CLOSER.add_closer(to_close)

def on_exit():
  EXIT_CLOSER.close()
