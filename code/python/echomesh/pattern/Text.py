from __future__ import absolute_import, division, print_function, unicode_literals

import cechomesh

from PIL import Image, ImageDraw, ImageFont

from echomesh.pattern.Pattern import Pattern
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class Text(Pattern):
  CONSTANTS =  'file', 'text', 'x', 'y',
  OPTIONAL_CONSTANTS = {
    'encoding': '',
    'index': 0,
    'oversample': 4,
    'x_offset': 0,
    'y_offset': 0,
    }
  PATTERN_COUNT = 0

  def _evaluate(self):
    oversample = self.get('oversample')
    x = self.get('x')
    y = self.get('y')
    x_over = oversample * x
    y_over = oversample * y
    im = Image.new('RGBA', (x_over, y_over))
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(self.get('file'), y_over)
    draw.text(xy=(self.get('x_offset'), self.get('y_offset')),
              text=self.get('text'), font=font)
    im = im.resize((x, y), resample=Image.ANTIALIAS)
    return cechomesh.ColorList(im)

