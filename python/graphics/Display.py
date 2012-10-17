from __future__ import absolute_import, division, print_function, unicode_literals

import pygame

class Display(object):
  def __init__(self, config):
    self.config = config
    pygame.init()
    dconf = config['display']
    full_screen = dconf['full_screen']
    if full_screen:
      flags = pygame.FULLSCREEN & pygame.NOFRAME
      resolution = 0, 0
    else:
      flags = 0
      resolution = dconf['width'], dconf['height']
    self.screen = pygame.display.set_mode(resolution, flags)

  def close(self):
    pygame.quit()
