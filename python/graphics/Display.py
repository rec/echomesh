from __future__ import absolute_import, division, print_function, unicode_literals

from util import Log
from util import Openable

LOGGER = Log.logger(__name__)

def display(echomesh, config):
  if config['display'].get('enable', True):
    library = config['display'].get('library', '(no library set in Config)')
    if library == 'pi3d':
      from graphics import Pi3dDisplay
      return Pi3dDisplay.Pi3dDisplay(echomesh, config)

    elif library == 'pygame':
      from graphics import PygameDisplay
      return PygameDisplay.PygameDisplay(echomesh, config)

    LOGGER.critical("No display library for '%s'", library)
    assert False
