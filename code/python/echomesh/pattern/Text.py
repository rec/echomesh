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

    font = get_font(fontfile, text, height, font_height)
    image = Image.new('RGBA', font.size)
    draw = ImageDraw.Draw(image)
    font.draw(draw)

    if debug:
      image.show()
    return cechomesh.ColorList(image, columns=font.size[0])


