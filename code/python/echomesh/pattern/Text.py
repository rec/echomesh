from __future__ import absolute_import, division, print_function, unicode_literals

import math

from PIL import Image, ImageDraw

import cechomesh

from echomesh.pattern.Pattern import Pattern
from echomesh.util.image.GetFont import get_font

class Text(Pattern):
  CONSTANTS =  'font', 'height', 'text'
  OPTIONAL_CONSTANTS = {'debug': False, 'oversample': 1, 'resample': None}
  PATTERN_COUNT = 0

  def _evaluate(self):
    fontfile = self.get('font')
    height = self.get('height')
    oversample = self.get('oversample')
    text = self.get('text')
    debug = self.get('debug')

    height_over = height * oversample
    font, size = get_font(fontfile, text, height_over)
    offset = font.getoffset(text)
    image = Image.new('RGBA', size)
    draw = ImageDraw.Draw(image)
    draw.text((-offset[0], -offset[1]), text=text, font=font)

    width = size[0]
    if oversample > 1:
      if debug:
        image.show()
      width = int(math.ceil(width / oversample))
      if resample:
        try:
          resample = getattr(Image, resample.upper())
        except:
          raise Exception("Don't understand resample=%s" % resample)
      else:
        resample = Image.BICUBIC
      image = image.resize((width, height), resample=resample)

    if debug:
      image.show()
    return cechomesh.ColorList(image, columns=width)
