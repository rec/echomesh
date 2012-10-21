from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import math
import pygame
# import pygame.sprite

from graphics import Path
from util import Openable

class ImagePath(pygame.sprite.DirtySprite):
  def __init__(self, image, angle, duration, display):
    pygame.sprite.DirtySprite.__init__(self)

    self.image = pygame.image.load(image)
    self.rect = self.image.get_rect()
    self.display = display

    # Inflate to the right and down by the width of the image.
    width = display.size[0] + self.rect.width
    height = display.size[1] + self.rect.height

    path = Path.path(angle, width, height)

    # Move back to the origin.
    for p in path:
      p[0] -= self.rect.width
      p[1] -= self.rect.height

    self.duration = duration * 1000.0
    self.start = 0

    self.begin, self.end = path
    self.rect.move_ip(self.begin)
    # print(dir(self.rect))

  def update(self, time):
    pygame.sprite.DirtySprite.update(self)
    self.display.dirty(self.rect)
    now = self.display.time
    if not self.start:
      self.start = now

    ratio = (now - self.start) / self.duration
    if ratio <= 1:
      x = self.begin[0] + (self.end[0] - self.begin[0]) * ratio
      y = self.begin[1] + (self.end[1] - self.begin[1]) * ratio
      self.rect.move_ip((x - self.rect.x, y - self.rect.y))
      self.dirty = 1
      self.display.dirty(self.rect)
    else:
      self.display.remove_sprite(self)
