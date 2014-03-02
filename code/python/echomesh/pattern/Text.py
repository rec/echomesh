from __future__ import absolute_import, division, print_function, unicode_literals

import math
from PIL import Image, ImageDraw, ImageFont

import cechomesh

from echomesh.pattern.Pattern import Pattern
from echomesh.util import Log

LOGGER = Log.logger(__name__)
_SUFFIX = '.ttf'

def _get_font(fontfile, text, height):
  new_height = height
  while True:
    try:
      font = ImageFont.truetype(fontfile, new_height)
    except:
      raise Exception('Can\'t open font file %s' % fontfile)
    size = font.getsize(text)
    if height >= size[1]:
      return font, size
    else:
      new_height -= 1

class Text(Pattern):
  CONSTANTS =  'font', 'height', 'text'
  OPTIONAL_CONSTANTS = {'oversample': 1, 'resample': None}
  PATTERN_COUNT = 0

  def _evaluate(self):
    fontfile = self.get('font')
    height = self.get('height')
    oversample = self.get('oversample')
    text = self.get('text')

    if not fontfile.endswith(_SUFFIX):
      fontfile += _SUFFIX

    height_over = height * oversample
    font, size = _get_font(fontfile, text, height_over)
    offset = font.getoffset(text)
    image = Image.new('RGBA', size)
    draw = ImageDraw.Draw(image)
    draw.text((-offset[0], -offset[1]), text=text, font=font)

    width = size[0]
    image.show()
    if oversample > 1:
      width = int(math.ceil(width / oversample))
      if resample:
        try:
          resample = getattr(Image, resample.upper())
        except:
          raise Exception("Don't understand resample=%s" % resample)
      else:
        resample = Image.BICUBIC
      image = image.resize((width, height), resample=resample)
      image.show()

    return cechomesh.ColorList(image, columns=width)
