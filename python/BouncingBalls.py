# Bouncing balls example using pi3d module
# ========================================
# Copyright (c) 2012 - Tim Skillman
# Version 0.02 - 03Jul12
#
# This example does not reflect the finished pi3d module in any way whatsoever!
# It merely aims to demonstrate a working concept in simplfying 3D programming on the Pi
#
# PLEASE INSTALL PIL imaging with:
#
#      $ sudo apt-get install python-imaging
#
# before running this example
#
# Bouncing demonstrates pi3d sprites over the desktop.
# It uses the orthographic view scaled to the size of the window;
# this means that sprites can be drawn at pixel resolution
# which is more common for 2D.  Also demonstrates a mock title bar.

from graphics.pi3d import pi3d
import sys, random, array

# Setup display and initialise pi3d
scnx=800
scny=600
display = pi3d.display()
display.create2D(100,100,scnx,scny,0)

ENABLE_CAPTION = not True

# Set last value (alpha) to zero for a transparent background!
display.setBackColour(1.0,0.2,0.6,1)

# Ball parameters
maxballs = 1
maxballsize = 60
minballsize = 30
maxspeed = 30

# Ball x,y position
bx=[]
by=[]

# Ball direction vector
dx=[]
dy=[]

# Ball size (scale), ball image reference
bs=[]
bi=[]

# Setup ball positions, sizes, directions and colours
for b in range (0, maxballs):
    bx.append(random.random() * scnx)
    by.append(random.random() * scny)
    dx.append((random.random() - 0.5) * maxspeed)
    dy.append((random.random() - 0.5) * maxspeed)
    bs.append(random.random() * maxballsize + minballsize)
    bi.append(int(random.random() * 3))

texs=pi3d.textures()
ball = []
ball.append(texs.loadTexture("graphics/pi3d/textures/red_ball.png"))
ball.append(texs.loadTexture("graphics/pi3d/textures/grn_ball.png"))
ball.append(texs.loadTexture("graphics/pi3d/textures/blu_ball.png"))
bar = texs.loadTexture("graphics/pi3d/textures/bar.png")
bbtitle = texs.loadTexture("graphics/pi3d/textures/pi3dbbd.png",True)

# Fetch key presses
scshots = 1
first_time = True

while True:

    display.clear()
    for b in range (0, maxballs):

	# Draw ball (tex,x,y,z,width,height,rotation)
        if first_time:
            print(ball[bi[b]],bx[b],by[b],-2.0,bs[b],bs[b])
        first_time = False
	pi3d.sprite(ball[bi[b]],bx[b],by[b],-2.0,bs[b],bs[b])

	# Increment ball positions
	bx[b]=bx[b]+dx[b]
	by[b]=by[b]+dy[b]

	# X coords outside of drawing area?  Then invert X direction
	if bx[b]>scnx or bx[b]<0:
		dx[b]=-dx[b]

	# Y coords outside of drawing area?  Then invert Y direction
	if by[b]>scny or by[b]<0:
		dy[b]=-dy[b]

    if ENABLE_CAPTION:
      #draw a bar at the top of the screen
      pi3d.rectangle(bar,0,scny,scnx,32)
      pi3d.rectangle(bbtitle,5,scny,256+5,32)

    display.swapBuffers()
