from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Log
from echomesh.util.thread.LockedList import LockedList
from echomesh.util.thread.Runnable import Runnable

LOGGER = Log.logger(__name__)

class RunnableOwner(Runnable):
  def __init__(self):
    super(RunnableOwner, self).__init__()
    self.runnables = LockedList()
    self.stoppables = LockedList()

  def add_slave(self, *slaves):
    self.runnables.add(*slaves)
    self.stoppables.add(*slaves)

  def remove_slave(self, *slaves):
    self.runnables.remove(*slaves)
    self.stoppables.remove(*slaves)

  def add_slave_closer(self, *clients):
    self.add_slave(*clients)
    for c in clients:
      c and c.stoppables.add(self)

  def start(self):
    super(RunnableOwner, self).start()
    self.runnables.foreach(lambda e: e.start())

  def stop(self):
    if self.is_running:
      super(RunnableOwner, self).stop()
      self.stoppables.foreach(lambda e: e.stop())

  def join(self):
    super(RunnableOwner, self).join()
    self.runnables.foreach(lambda e: e.join())
