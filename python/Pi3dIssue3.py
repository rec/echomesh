from graphics.pi3d import pi3d

import sys, random, array

ENABLE_BUG = not True

scnx = 800
scny = 600

def init_display():
  DISPLAY.create2D(100,100,scnx,scny,0)
  DISPLAY.setBackColour(1.0,0.2,0.6,1)

DISPLAY = pi3d.display()
if not ENABLE_BUG:
  init_display()

class Display(object):
  def __init__(self):
    self.texs = pi3d.textures()
    self.ball = self.texs.loadTexture("graphics/pi3d/textures/red_ball.png")
    if ENABLE_BUG:
      init_display()

  def run(self):
    while True:
      DISPLAY.clear()
      pi3d.sprite(self.ball, 200.0, 200.0, -2.0, 80.0, 80.0)
      DISPLAY.swapBuffers()

Display().run()
