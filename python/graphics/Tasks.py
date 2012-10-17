from __future__ import absolute_import, division, print_function, unicode_literals

from util import Openable


class Flipper(Openable.Openable):
  def update(self, time):
    pygame.display.flip()


class Clearer(Openable.Openable):
  def __init__(self, display, color=(0, 0, 0)):
    Openable.Openable.__init__(self)
    self.display = display
    self.color = color

  def update(self, time):
    self.display.screen.fill(self.color)