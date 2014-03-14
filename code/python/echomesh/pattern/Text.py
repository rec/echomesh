from __future__ import absolute_import, division, print_function, unicode_literals

import cechomesh

from echomesh.pattern.Pattern import Pattern
from echomesh.util.image.DrawText import draw_text

class Text(Pattern):
  SETTINGS = {
    'font': {
      'default': '',
      'help': '',
      },
    'text': {
      'default': '',
      'help': '',
      },
    'debug': {
      'default': False,
      'help': '',
      },
    'height': {
      'default': 0,
      'help': '',
      },
    'font_height': {
      'default': 0,
      'help': '',
      },
    }
  PATTERN_COUNT = 0

  def _evaluate(self):
    debug = self.get('debug')
    fontfile = self.get('font')
    if not fontfile:
      raise ValueError("Text doesn't have a font setting")
    font_height = self.get('font_height')
    height = self.get('height') or font_height
    text = self.get('text')
    if not text:
      raise ValueError("Text doesn't have a text setting")

    image, width, height = draw_text(fontfile, text, height, font_height)
    if debug:
      print('width=%d, height=%d' % (width, height))
      image.show()
    return cechomesh.ColorList(image, columns=width)
