from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Settings
from echomesh.element import Element
from echomesh.sound.CPlayer import CPlayer
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class Audio(Element.Element):
  def __init__(self, parent, description):
    super(Audio, self).__init__(parent, description)
    if Settings.get('audio', 'output', 'enable'):
      try:
        self.add_mutual_pause_slave(CPlayer(self, **description))
      except:
        LOGGER.error()
    else:
      LOGGER.info('Audio disabled for %s', description.get('file', None))
    description.clear_accessed()
