from __future__ import absolute_import, division, print_function, unicode_literals

from config import Config
from util import Log

from util.ThreadLoop import ThreadLoop
from graphics.pi3d import pi3d

LOGGER = Log.logger(__name__)

scnx=800
scny=600

DEFAULT_BACKGROUND = 1.0, 0.2, 0.6, 1
DEFAULT_DIMENSIONS = 100, 100, scnx, scny, 0

def display(echomesh, config):
  if Config.is_enabled('display'):
    library = config['display'].get('library', '(no library set in Config)')
    if library == 'pi3d':
      from graphics import Pi3dDisplay
      return Pi3dDisplay.Pi3dDisplay(echomesh, config)

    elif library == 'pygame':
      from graphics import PygameDisplay
      return PygameDisplay.PygameDisplay(echomesh, config)

    LOGGER.critical("No display library for '%s'", library)
    assert False
