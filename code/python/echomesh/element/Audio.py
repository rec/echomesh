from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Config
from echomesh.util import Log
from echomesh.element import Element
from echomesh.element import Register

LOGGER = Log.logger(__name__)

class Audio(Element.Element):
  def __init__(self, parent, description):
    super(Audio, self).__init__(parent, description)
    if Config.get('audio', 'output', 'enable'):
      from echomesh.sound import FilePlayer
      self.add_openable_mutual(FilePlayer.play(**description['keywords']))
    else:
      LOGGER.info('Playing audio')

Register.register(Audio)
