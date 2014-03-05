from __future__ import absolute_import, division, print_function, unicode_literals

import math

from PIL import Image, ImageDraw

import cechomesh

from echomesh.pattern.Pattern import Pattern
from echomesh.util.image.GetFont import get_font

class Text(Pattern):
  CONSTANTS =  'font', 'text'
  OPTIONAL_CONSTANTS = {
    'debug': False,
    'height': 0,
    'font_height': 0,
    }
  PATTERN_COUNT = 0

  def _evaluate(self):
    fontfile = self.get('font')
    height = self.get('height')
    font_height = self.get('font_height')
    text = self.get('text')
    debug = self.get('debug')
    height = height or font_height

    font, size, offset = get_font(fontfile, text, height, font_height)
    image = Image.new('RGBA', size)
    draw = ImageDraw.Draw(image)
    draw.text((-offset[0], -offset[1]), text=text, font=font)

    if debug:
      image.show()
    return cechomesh.ColorList(image, columns=size[0])


