from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Config
from echomesh.element import Element
from echomesh.graphics.ImageSprite import ImageSprite
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class Image(Element.Element):
  def __init__(self, parent, description):
    super(Image, self).__init__(parent, description)
    if Config.get('load_module', 'pi3d'):
      try:
        self.sprite = ImageSprite(**description)
      except Exception as e:
        LOGGER.error("Couldn't open image file")
      else:
        self.add_slave(self.sprite)
    else:
      LOGGER.info('Playing image %s', description.get('file', '(none)'))

Element.register(Image)
