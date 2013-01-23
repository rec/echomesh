from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.element import Element
from echomesh.util.thread import TimeLoop

class Loop(Element.Element):
  def __init__(self, parent, description, name='Element.Loop'):
    super(Loop, self).__init__(parent, description)
    self.loop = TimeLoop.TimeLoop(name=name)
    self.add_openable_mutual(self.loop)
