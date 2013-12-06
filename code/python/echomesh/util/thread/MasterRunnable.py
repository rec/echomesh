from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util.thread.LockedList import LockedList
from echomesh.util.thread.Runnable import Runnable
from echomesh.base import Quit

class MasterRunnable(Runnable):
  """A Runnable that controls a list of other runnables.
  """
  def __init__(self):
    super(MasterRunnable, self).__init__()
    self.runnables = LockedList()
    self.pausables = LockedList()
    self.joinables = LockedList()

  def add_slave(self, *slaves):
    """Adds one or more slaves - Runnables that run, pause and join
    when this one does."""
    self.runnables.add(*slaves)
    self.pausables.add(*slaves)
    self.joinables.add(*slaves)

  def add_pause_only_slave(self, *slaves):
    self.pausables.add(*slaves)
    self.joinables.add(*slaves)

  def remove_slave(self, *slaves):
    self.runnables.remove(*slaves)
    self.pausables.remove(*slaves)
    self.joinables.remove(*slaves)

  def add_mutual_pause_slave(self, *clients):
    self.add_slave(*clients)
    for c in clients:
      if c:
        c.pausables.add(self)

  def run(self):
    super(MasterRunnable, self).run()
    self.runnables.foreach('run')

  def pause(self):
    try:
      if self.is_running:
        self.is_running = False
        self.pausables.foreach('pause')
        self.is_running = True
      super(MasterRunnable, self).pause()
    except:
      if not Quit.QUITTING:
        raise

  def begin(self):
    super(MasterRunnable, self).begin()
    self.runnables.foreach('begin')

  def unload(self):
    super(MasterRunnable, self).unload()
    self.runnables.foreach('unload')
