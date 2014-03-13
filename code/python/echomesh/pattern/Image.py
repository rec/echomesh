from __future__ import absolute_import, division, print_function, unicode_literals

import PIL.Image

import cechomesh

from echomesh.pattern.Pattern import Pattern
from echomesh.util import Log
from echomesh.util.image.Crop import crop
from echomesh.util.image.Resize import resize

LOGGER = Log.logger(__name__)

class Image(Pattern):
  SETTINGS = {
    'bottom_offset': {'default': 0},
    'left': {'default': None},
    'left_offset': {'default': 0},
    'right_offset': {'default': 0},
    'stretch': {'default': False},
    'top': {'default': None},
    'top_offset': {'default': 0},
    'filename': {'default': 0, 'constant': True},
    'x': {'default': 0, 'constant': True},
    'y': {'default': 0, 'constant': True},
    }

  PATTERN_COUNT = 0

  def _get_image(self):
    filename = self.get('filename')
    if not filename:
      raise Exception('Missing filename setting in Image pattern.')
    return PIL.Image.open(filename, 'r')

  def _evaluate(self):
    return self._image_to_list(self._get_image())

  def _image_to_list(self, image):
    if image.mode != 'RGB':
      image = image.convert(mode='RGB')

    image = crop(image, **self.get_dict(
      'top_offset', 'left_offset', 'bottom_offset', 'right_offset'))
    image = resize(image, **self.get_dict('x', 'y', 'stretch', 'top', 'left'))
    return cechomesh.ColorList(image)
