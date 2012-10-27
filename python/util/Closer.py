from __future__ import absolute_import, division, print_function, unicode_literals

import weakref

from util import Log
from util.Openable import Openable

LOGGER = Log.logger(__name__)

class Closer(Openable):
  def __init__(self, *closers):
    Openable.__init__(self)
    self.closers = weakref.WeakSet(closers)

  def add_closer(self, *closers):
    self.closers.update(closers)

  def close(self):
    Openable.close(self)
    for c in self.closers:
      try:
        if c and c.is_open:
          c.close()
      except:
        LOGGER.error("Couldn't close %s" % repr(c))

  def join(self):
    for c in self.closers:
      try:
        c.join()
      except:
        pass

