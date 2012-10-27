from __future__ import absolute_import, division, print_function, unicode_literals

import time

from graphics import Rect
from graphics.pi3d import pi3d

from util import Log
from util.ThreadLoop import ThreadLoop

LOGGER = Log.logger(__name__)

DEFAULT_BACKGROUND = 0, 0, 0, 1.0
ESCAPE_KEY = 27
DEFAULT_FPS = 60.0
READ_KEYS = False
DISABLE = True

# Setup display and initialise pi3d
scnx = 800
scny = 600

display = pi3d.display()

display.create2D(100,100,scnx,scny,0)

# Set last value (alpha) to zero for a transparent background!
display.setBackColour(1.0,0.2,0.6,1)

texs = pi3d.textures()

bbtitle = texs.loadTexture("graphics/pi3d/textures/pi3dbbd.png",True)

class Pi3dDisplay(ThreadLoop):
  def __init__(self, echomesh, config):
    ThreadLoop.__init__(self)

  def run(self):
    print('here!')
    display.clear()
    pi3d.rectangle(bbtitle,5,scny,256+5,32)
    display.swapBuffers()
