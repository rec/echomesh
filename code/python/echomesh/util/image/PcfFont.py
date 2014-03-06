from __future__ import absolute_import, division, print_function, unicode_literals

from PIL import Image, PcfFontFile

from echomesh.util import Log

LOGGER = Log.logger(__name__)
INFINITY = float('inf')

def draw_pcf(fontfile, text, height, font_height):
  if height or font_height:
    LOGGER.warning("You can't set a height or font_height for .pcf fonts")
  with open(fontfile, 'rb') as f:
    font = PcfFontFile.PcfFontFile(f)

  def glyph(ch):
    try:
      return font.glyph[ord(ch)]
    except IndexError:
      return font.glyph[0]

  x, y, width, height = INFINITY, INFINITY, 0, 0
  for ch in text:
    off_x, off_y, w, h = glyph(ch)[2]
    x = min(x, off_x)
    y = min(y, off_y)
    width += w
    height = max(height, h)

  image = Image.new('RGBA', (width, height))
  for ch in text:
    g = glyph(ch)
    image.paste(g[3], box=(x, y))
    x += g[2][2]
  return image, width, height

