from __future__ import absolute_import, division, print_function, unicode_literals

import pygame
import sys

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


class Quitter(Openable.Openable):
  def update(self, time):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        # TODO: why isn't this working?
        # TODO: use the standard quitting mechanism.
        sys.exit()
