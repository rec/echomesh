from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.Cechomesh import cechomesh

from echomesh.pattern.Pattern import Pattern
from echomesh.util.image.DrawText import draw_text

class Text(Pattern):
    HELP = """Display text on an x-y grid in either a PCF or Truetype font.
  PCF fonts are less common but give better results. Truetype (ttf) fonts are
  more common but often require experimentation to get the right size.

  PCF fonts are fixed size so you don't have to set anything other than the font
  and the text.  For Truetype fonts, you need to specify either the height - the
  desired output height for the text - or the font_height - the specific height
  of the font itself (the actual text you display is likely shorter than that
  unless it includes both ascenders and descenders of maximum size).
  """
    SETTINGS = {
      'font': {
        'default': '',
        'help': ("The name of the file containing the font.  If you don\t ",
                 "include a suffix, the program tries first .pcf then .ttf."),
        },
      'text': {
        'default': '',
        'help': 'The actual text to be displayed.',
        },
      'debug': {
        'default': False,
        'help': ('If true, echomesh tries to pop up an external display '
                 'for the image containing the rendered text.'),
        },
      'height': {
        'default': 0,
        'help': 'The desired height of the output text, in pixels.',
        },
      'font_height': {
        'default': 0,
        'help': ('The full height of the font itself.  This is used as a hint '
                 'to get better results for Truetype fonts.'),
        },
      }

    CONSTANT = True

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
        return cechomesh.ColorMatrix(image, columns=width)
