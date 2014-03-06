from __future__ import absolute_import, division, print_function, unicode_literals

import cechomesh

from echomesh.pattern.Pattern import Pattern
from echomesh.util.image.DrawText import draw_text

class Text(Pattern):
  CONSTANTS =  'font', 'text'
  OPTIONAL_CONSTANTS = {
    'debug': False,
    'height': 0,
    'font_height': 0,
    }
  PATTERN_COUNT = 0

  def _evaluate(self):
    debug = self.get('debug')
    fontfile = self.get('font')
    font_height = self.get('font_height')
    height = self.get('height') or font_height
    text = self.get('text')

    image, width = draw_text(fontfile, text, height, font_height)
    if debug:
      image.show()
    return cechomesh.ColorList(image, columns=width)
