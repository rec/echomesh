from __future__ import absolute_import, division, print_function, unicode_literals

import PIL.Image

import cechomesh

from echomesh.pattern.Pattern import Pattern
from echomesh.util import Log
from echomesh.util.image import Resize

LOGGER = Log.logger(__name__)

class Image(Pattern):
  CONSTANTS = 'filename', 'x', 'y',
  OPTIONAL_CONSTANTS = {
    'bottom_offset': 0,
    'left': None,
    'left_offset': 0,
    'right_offset': 0,
    'stretch': False,
    'top': None,
    'top_offset': 0,
    }
  PATTERN_COUNT = 0

  def _get_image(self):
    return PIL.Image.open(self.get('filename'), 'r')

  def _evaluate(self):
    return self._image_to_list(self._get_image())

  def _image_to_list(self, image):
    parts = self.get_all('x', 'y', 'stretch', 'top', 'left',
                         'top_offset', 'left_offset',
                         'bottom_offset', 'right_offset')
    if image.mode != 'RGB':
      image = image.convert(mode='RGB')
    return cechomesh.ColorList(Resize.resize(image, *parts).getdata())
