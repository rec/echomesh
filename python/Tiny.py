from graphics.pi3d import pi3d
import sys, random, array

# Setup display and initialise pi3d
scnx=800
scny=600
display = pi3d.display()
display.create2D(100,100,scnx,scny,0)

# Set last value (alpha) to zero for a transparent background!
display.setBackColour(1.0,0.2,0.6,1)

texs = pi3d.textures()
ball = texs.loadTexture("graphics/pi3d/textures/red_ball.png")

while True:

    display.clear()
    pi3d.sprite(ball, 400, 400, -2.0, 41, 41)
    display.swapBuffers()
