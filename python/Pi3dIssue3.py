from graphics.pi3d import pi3d

import sys, random, array

ENABLE_BUG = True

scnx = 800
scny = 600

DISPLAY = pi3d.display()

DISPLAY.create2D(100,100,scnx,scny,0)

# Set a pink display
DISPLAY.setBackColour(1.0,0.2,0.6,1)

texs=pi3d.textures()
ball = texs.loadTexture("graphics/pi3d/textures/red_ball.png")

while True:
  DISPLAY.clear()
  pi3d.sprite(ball, 200.0, 200.0, -2.0, 80.0, 80.0)
  DISPLAY.swapBuffers()
