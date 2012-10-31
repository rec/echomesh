from graphics.pi3d import pi3d

import sys, random, array

ENABLE_BUG = True

scnx = 800
scny = 600

def init(disp):
  disp.create2D(100,100,scnx,scny,0)
  disp.setBackColour(1.0,0.2,0.6,1)
  return disp

def init_display():
  return init(pi3d.display())

if not ENABLE_BUG:
  DISPLAY = init_display()


class Display(object):
  def __init__(self):
    self.texs = pi3d.textures()
    self.ball = self.texs.loadTexture("graphics/pi3d/textures/red_ball.png")
    if ENABLE_BUG:
      self.display = pi3d.display()
      init(self.display)
    else:
      self.display = DISPLAY

  def run(self):
    while True:
      self.display.clear()
      pi3d.sprite(self.ball, 200.0, 200.0, -2.0, 80.0, 80.0)
      self.display.swapBuffers()

Display().run()
