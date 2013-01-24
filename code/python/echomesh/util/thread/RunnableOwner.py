from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Log
from echomesh.util.thread.LockedList import LockedList
from echomesh.util.thread.Runnable import Runnable

LOGGER = Log.logger(__name__)

class RunnableOwner(Runnable):
  def __init__(self):
    super(RunnableOwner, self).__init__()
    self.openables = LockedList()
    self.closeables = LockedList()

  def add_slave(self, *slaves):
    self.openables.add(*slaves)
    self.closeables.add(*slaves)

  def remove_slave(self, *slaves):
    self.openables.remove(*slaves)
    self.closeables.remove(*slaves)

  def add_slave_closer(self, *clients):
    self.add_slave(*clients)
    for c in clients:
      c and c.closeables.add(self)

  def start(self):
    super(RunnableOwner, self).start()
    self.openables.foreach(lambda e: e.start())

  def close(self):
    if self.is_running:
      super(RunnableOwner, self).close()
      self.closeables.foreach(lambda e: e.close())

  def join(self):
    super(RunnableOwner, self).join()
    self.openables.foreach(lambda e: e.join())
