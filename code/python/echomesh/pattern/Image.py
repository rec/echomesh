from __future__ import absolute_import, division, print_function, unicode_literals

import PIL.Image

import cechomesh

from echomesh.pattern.Pattern import Pattern
from echomesh.util import Log
from echomesh.util.image.Crop import crop
from echomesh.util.image.Resize import resize

LOGGER = Log.logger(__name__)

class Image(Pattern):
  HELP = """Displays an image on an x, y plane.
Image accepts JPG, GIF and PNG files."""

  SETTINGS = {
    'bottom_offset': {
      'default': 0,
      'help': 'How many pixels to crop off the bottom of the image.',
      },
    'left': {
      'default': None,
      'help': ('If None, then the image is horizontally centered - if true, '
               'the image is left justified, otherwise it\'s right justified.'),
      },
    'left_offset': {
      'default': 0,
      'help': 'How many pixels to crop off the left of the image.',
      },
    'right_offset': {
      'default': 0,
      'help': 'How many pixels to crop off the right of the image.',
      },
    'stretch': {
      'default': False,
      'help': ('If true, the image is stretched to fit the pane, ignoring '
               'the aspect ratio '),
      },
    'top': {
      'default': None,
      'help': ('If None, then the image is vertically centered - if true, '
               'the image is top justified, otherwise it\'s bottom justified.'),
      },
    'top_offset': {
      'default': 0,
      'help': 'How many pixels to crop off the top of the image.',
      },
    'filename': {
      'default': 0, 'constant': True,
      'help': 'Filename for the image file.',
      },
    'x': {
      'default': 0,
      'constant': True,
      'help': 'Width of the result, in pixels.',
      },
    'y': {
      'default': 0,
      'constant': True,
      'help': 'Height of the result, in pixels.',
      },
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
