from __future__ import absolute_import, division, print_function, unicode_literals

from config import Config
from util import Log

from util.ThreadLoop import ThreadLoop
from graphics.pi3d import pi3d

LOGGER = Log.logger(__name__)
DEBUGGING = True

scnx=800
scny=600

DEFAULT_BACKGROUND = 1.0, 0.2, 0.6, 1
DEFAULT_DIMENSIONS = 100, 100, scnx, scny, 0

DISPLAY = pi3d.display()
DISPLAY.create2D(*DEFAULT_DIMENSIONS)

# Set last value (alpha) to zero for a transparent background!
DISPLAY.setBackColour(*DEFAULT_BACKGROUND)

texs = pi3d.textures()
ball = texs.loadTexture("graphics/pi3d/textures/red_ball.png")

class DebugDisplay(ThreadLoop):
  def __init__(self, echomesh, config):
    ThreadLoop.__init__(self)
    self.config = config
    self.echomesh = echomesh
    self.textures = pi3d.textures()
    self.texture_cache = {}
    self.sprites = []

    dconf = config['display']

    background = dconf.get('background', DEFAULT_BACKGROUND)
    dimensions = dconf.get('dimensions', DEFAULT_DIMENSIONS)
    #self.display = pi3d.display()
    #self.display.create2D(*background)
    #self.display.setBackColour(*dimensions)

  def add_sprite(self, sprite):
    pass

  def run(self):
    DISPLAY.clear()
    pi3d.sprite(ball, 400, 400, -2.0, 41, 41)
    DISPLAY.swapBuffers()

  def close(self):
    LOGGER.error('Closing display!')
    ThreadLoop.close(self)

  def load_texture(self, imagefile):
    pass

def display(echomesh, config):
  if Config.is_enabled(config, 'display'):
    if DEBUGGING:
      return DebugDisplay(echomesh, config)

    library = config['display'].get('library', '(no library set in Config)')
    if library == 'pi3d':
      from graphics import Pi3dDisplay
      return Pi3dDisplay.Pi3dDisplay(echomesh, config)

    elif library == 'pygame':
      from graphics import PygameDisplay
      return PygameDisplay.PygameDisplay(echomesh, config)

    LOGGER.critical("No display library for '%s'", library)
    assert False
