from __future__ import absolute_import, division, print_function, unicode_literals

import math
from PIL import Image, ImageDraw, ImageFont

import cechomesh

from echomesh.pattern.Pattern import Pattern
from echomesh.util import Log

LOGGER = Log.logger(__name__)
_SUFFIX = '.ttf'

class Text(Pattern):
  CONSTANTS =  'font', 'size', 'text'
  OPTIONAL_CONSTANTS = {'oversample': 4,}
  PATTERN_COUNT = 0

  def _evaluate(self):
    fontfile = self.get('font')
    height = self.get('size')
    oversample = self.get('oversample')
    text = self.get('text')

    if not fontfile.endswith(_SUFFIX):
      fontfile += _SUFFIX

      height_over = height * oversample
    try:
      font = ImageFont.truetype(fontfile, height_over)
    except:
      raise Exception('Can\'t open font file %s' % fontfile)
    size = font.getsize(text)
    image = Image.new('RGBA', size)
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text=text, font=font)

    columns = int(math.ceil(size[0] / oversample))
    rows = int(math.ceil(size[1] / oversample))
    image = image.resize((columns, rows), resample=Image.ANTIALIAS)
    return cechomesh.ColorList(image, columns=columns)
