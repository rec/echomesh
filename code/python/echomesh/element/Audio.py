from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Config
from echomesh.util import Log
from echomesh.element import Element

LOGGER = Log.logger(__name__)

class Audio(Element.Element):
  def __init__(self, parent, description):
    super(Audio, self).__init__(parent, description)
    if Config.get('audio', 'output', 'enable'):
      try:
        from echomesh.sound import Play
        self.add_mutual_pause_slave(Play.play(self, **description))
      except:
        LOGGER.error()
    else:
      LOGGER.info('Audio disabled for %s', description.get('file', None))
    description.clear_accessed()

