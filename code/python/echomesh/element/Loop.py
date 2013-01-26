from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.element import Element
from echomesh.util.thread import TimeLoop

class Loop(Element.Element):
  def __init__(self, parent, description, interval=1, name='Element.Loop'):
    super(Loop, self).__init__(parent, description)
    self.time_loop = TimeLoop.TimeLoop(
      name=name,
      interval=interval,
      next_time=getattr(self, 'next_time', None),
      loop_target=getattr(self, 'loop_target', None))

    self.add_mutual_stop_slave(self.time_loop)

  # You can implement Loop.next_time and Loop.loop to override the methods in
  # TimeLoop.
