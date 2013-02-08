from __future__ import absolute_import, division, print_function, unicode_literals

import pygame
import sys
import time

from echomesh.graphics import Display
from echomesh.graphics import Path

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

WIDTH = 400
HEIGHT = 400
MIDDLE = (WIDTH / 2.0, HEIGHT / 2.0)

READ_INPUT = False

display = Display.Display(dict(display=dict(full_screen=False,
                                            width=WIDTH, height=HEIGHT)))
display.start()
screen = display.screen

degrees = -1

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()

  if READ_INPUT:
    degrees = raw_input()
  else:
    degrees += 1
  screen.fill(BLACK)

  if degrees == '':
    sys.exit()

  begin, end = Path.path(int(degrees), WIDTH, HEIGHT)

  # print(begin, end)
  # print(degrees)

  pygame.draw.line(screen, RED, begin, MIDDLE)
  pygame.draw.line(screen, GREEN, MIDDLE, end)
  pygame.display.flip()

  #if degrees in [134, 135, 136]:
  #  time.sleep(1.0)
