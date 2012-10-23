from __future__ import absolute_import, division, print_function, unicode_literals

from graphics.pi3d import pi3d

from util import Openable

class Pi3dDisplay(Openable.Openable):
  def __init__(self, config):
    Openable.Openable.__init__(self)
    self.config = config
    self.display = pi3d.display()
    display.create2D(x, y, width, height)
    display.setBackColor(0, 0, 0, 0)  # last is alpha

  def run(self):
    pass
