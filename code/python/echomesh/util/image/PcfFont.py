from __future__ import absolute_import, division, print_function, unicode_literals

from PIL import PcfFontFile

from echomesh.util import Log

LOGGER = Log.logger(__name__)

class PcfFont(object):
  def __init__(self, fontfile, text, height, font_height):
    self.text = text
    if height or font_height:
      LOGGER.warning("You can't set a height or font_height for .pcf fonts")
    with open(fontfile, 'rb') as f:
      self.font = PcfFontFile.PcfFontFile(f)
    offset_x, offset_y, width, height = INFINITY, INFINITY, 0, 0
    for ch in text:
      try:
        glyph = font.glyph[ord(ch)]
      except IndexError:
        glyph = font.glyph[0]
      off_x, off_y, w, h= glyph[2]
      offset_x = min(offset_x, off_x)
      offset_y = min(offset_y, off_y)
      width += w
      height = max(height, h)
    self.size = width, height
    self.offset = offset_x, offset_y

  def draw(self, drawable):
    pass
