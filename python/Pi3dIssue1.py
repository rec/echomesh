from graphics.pi3d import pi3d

import sys, random, array

ENABLE_BUG = True

scnx = 800
scny = 600

display = pi3d.display()

display.create2D(100,100,scnx,scny,0)

# Set a pink display
display.setBackColour(1.0,0.2,0.6,1)

while True:
  display.clear()
  if not ENABLE_BUG:
    pi3d.rectangle(None, 5, scny, 256+5, 32)
  display.swapBuffers()
