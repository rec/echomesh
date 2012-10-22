from __future__ import absolute_import, division, print_function, unicode_literals

from util import Log
from util import Openable

LOGGER = Log.logger(__name__)

DEFAULT_LIBRARY = 'pi3d'

def display(config):
  if config['display'].get('enable', True):
    library = config['display'].get('library', DEFAULT_LIBRARY)
    if library == 'pi3d':
      from graphics import Pi3dDisplay
      return Pi3dDisplay.Pi3dDisplay(config)

    elif library == 'pygame':
      from graphics import PygameDisplay
      return PygameDisplay.PygameDisplay(config)

    LOGGER.critical("Didn't understand display library '%s'", library)
    assert False
