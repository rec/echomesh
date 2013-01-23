from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Config
from echomesh.util import Log
from echomesh.element import Element
from echomesh.element import Register

LOGGER = Log.logger(__name__)

class Image(Element.Element):
  def __init__(self, parent, description):
    super(Image, self).__init__(parent, description)
    if Config.get('pi3d', 'enable'):
      from echomesh.graphics.Sprite import ImageSprite
      ImageSprite(**description)
    else:
      LOGGER.info('Playing image %s', keywords.get('image', '(none)'))

Register.register(Image)
