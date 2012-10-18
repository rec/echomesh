from __future__ import absolute_import, division, print_function, unicode_literals

import pygame

from util import ThreadLoop

class Display(ThreadLoop.ThreadLoop):
  def __init__(self, config, background_color=None):
    ThreadLoop.ThreadLoop.__init__(self)
    self.config = config
    self.clock = pygame.time.Clock()
    self.background_color = background_color or (0, 0, 0)

    pygame.init()
    dconf = self.config['display']
    full_screen = dconf['full_screen']
    if full_screen:
      flags = pygame.FULLSCREEN & pygame.NOFRAME
      resolution = 0, 0
    else:
      flags = 0
      resolution = dconf['width'], dconf['height']
    self.screen = pygame.display.set_mode(resolution, flags)
    self.size = self.screen.get_size()

    background = pygame.Surface(self.size).convert()
    background.fill(self.background_color)
    self.screen.blit(background, (0, 0))
    pygame.display.flip()

    self.sprites = pygame.sprite.LayeredDirty()
    self.sprites.clear(self.screen, background)
    self.time = 0.0

  def runnable(self):
    for e in pygame.event.get():
      if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and
                                   e.key == pygame.K_ESCAPE):
        self.close()
        return
    self.sprites.update(self.time)
    pygame.display.update(self.sprites.draw(self.screen))
    self.time += self.clock.tick(self.config['frames_per_second'])

  def close(self):
    ThreadLoop.ThreadLoop.close(self)
    pygame.quit()
