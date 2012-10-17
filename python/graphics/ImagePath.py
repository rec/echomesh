from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import math
import pygame

from graphics import Path
from util import Openable

def _length(x, y):
  return math.sqrt(x * x + y + y)

def _distance(p, q):
  return _length(q[0] - p[0], q[1] - p[1])


class ImagePath(Openable.Openable):
  def __init__(self, image, angle, duration, display):
    Openable.Openable.__init__(self)
    self.image = pygame.image.load(image)
    self.display = display
    self.rect = self.image.get_rect()

    width = display.size[0] + self.rect.width
    height = display.size[1] + self.rect.height
    path = Path.path(angle, width, height)  # self.begin, self.end

    for p in path:
      p[0] -= self.rect.width
      p[1] -= self.rect.height

    # distance = _distance(*path)
    self.duration = duration
    self.start = 0

    self.begin, self.end = path
    self.rect.move_ip(self.begin)

    print(angle, self.rect, self.begin, self.end)

  def update(self, now):
    if not self.start:
      self.start = now

    ratio = (now - self.start) / self.duration
    if ratio <= 1:
      x = self.begin[0] + (self.end[0] - self.begin[0]) * ratio
      y = self.begin[1] + (self.end[1] - self.begin[1]) * ratio
      self.rect.move_ip((x - self.rect.x, y - self.rect.y))
      self.display.screen.blit(self.image, self.rect)

    else:
      self.close()
