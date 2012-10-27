from graphics.pi3d import pi3d

import sys, random, array

# Setup display and initialise pi3d
scnx=800
scny=600

display = pi3d.display()

display.create2D(100,100,scnx,scny,0)

# Set last value (alpha) to zero for a transparent background!
display.setBackColour(1.0,0.2,0.6,1)

texs=pi3d.textures()

bar = texs.loadTexture("graphics/pi3d/textures/bar.png")
bbtitle = texs.loadTexture("graphics/pi3d/textures/pi3dbbd.png",True)

# Fetch key presses
mykeys = pi3d.key()

while True:

    display.clear()
    pi3d.rectangle(bar,0,scny,scnx,32)
    pi3d.rectangle(bbtitle,5,scny,256+5,32)

    display.swapBuffers()
