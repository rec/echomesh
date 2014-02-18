from __future__ import absolute_import, division, print_function, unicode_literals

import PIL.Image

import cechomesh

from echomesh.util.image import Resize
from echomesh.util import Log
from echomesh.pattern.Pattern import Pattern

LOGGER = Log.logger(__name__)

class Image(Pattern):
  CONSTANTS = 'filename', 'x', 'y',
  OPTIONAL_CONSTANTS = {'top': None, 'left': None, 'stretch': False}
  PATTERN_COUNT = 0

  def _evaluate(self):
    image = PIL.Image.open(self.get('filename'))
    return self._image_to_list(image)

  def _image_to_list(self, image):
    parts = self.get_all('x', 'y', 'stretch', 'top', 'left')
    return cechomesh.ColorList(Resize.resize(image, *parts).getdata())
