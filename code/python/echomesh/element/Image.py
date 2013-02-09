from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Config
from echomesh.util import Log
from echomesh.element import Element

LOGGER = Log.logger(__name__)

class Image(Element.Element):
  def __init__(self, parent, description):
    super(Image, self).__init__(parent, description)
    if Config.get('pi3d', 'enable'):
      from echomesh.graphics.ImageSprite import ImageSprite
      try:
        self.sprite = ImageSprite(**description)
      except Exception as e:
        LOGGER.error('%s', str(e))
      else:
        self.add_slave(self.sprite)
    else:
      LOGGER.info('Playing image %s', description.get('file', '(none)'))

Element.register(Image)
