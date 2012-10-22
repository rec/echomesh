from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import pygame

from graphics import ImagePath

from util import Log
from util import Platform
from util import ThreadLoop

if Platform.IS_MAC:
  IMAGE = '/development/echomesh/data/ball.gif'
else:
  IMAGE = '~/echomesh/data/ball.gif'


LOGGING = Log.logger(__name__)

def _make_screen(config):
  dconf = config['display']
  full_screen = dconf['full_screen']
  if full_screen:
    flags = pygame.FULLSCREEN & pygame.NOFRAME
    resolution = 0, 0
  else:
    flags = 0
    resolution = dconf['width'], dconf['height']
  return pygame.display.set_mode(resolution, flags)


class PygameDisplay(ThreadLoop.ThreadLoop):
  def __init__(self, config, background_color=None):
    ThreadLoop.ThreadLoop.__init__(self)
    self.config = config
    self.clock = pygame.time.Clock()
    self.background_color = background_color or (0, 0, 0)
    self.update_clients = []

    pygame.init()

    self.sprites = pygame.sprite.LayeredDirty()
    self.time = 0.0

    try:
      self.screen = _make_screen(config)
    except:
      self.screen = None
      LOGGING.error("Couldn't open graphics")
      return
    self.size = self.screen.get_size()

    background = pygame.Surface(self.size).convert()
    background.fill(self.background_color)
    self.screen.blit(background, (0, 0))
    pygame.display.flip()

    self.sprites.clear(self.screen, background)
    self._dirty = None
    p = ImagePath.ImagePath(IMAGE, 45, 10.0, self)
    self.add_sprite(p)


  def add_sprite(self, sprite):
    self.sprites.add(sprite)

  def remove_sprite(self, sprite):
    self.sprites.remove(sprite)

  def add_client(self, client):
    if client not in self.clients:
      self.update_clients.append(client)

  def remove_client(self, client):
    self.update_clients.remove(client)

  def dirty(self, rect):
    if self._dirty:
      self._dirty.union_ip(rect)
    else:
      self._dirty = copy.deepcopy(rect)

  def runnable(self):
    for c in self.update_clients:
      c.update(self.time)

    if not self.screen:
      return

    for e in pygame.event.get():
      if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and
                                   e.key == pygame.K_ESCAPE):
        self.close()
        return

    self._dirty = None
    self.sprites.update(self.time)
    rect = self.sprites.draw(self.screen)
    pygame.display.update(self._dirty)
    self.time += self.clock.tick(self.config['frames_per_second'])

  def close(self):
    ThreadLoop.ThreadLoop.close(self)
    pygame.quit()
