from __future__ import absolute_import, division, print_function, unicode_literals

from PIL import ImageFont

MIN_FONT_HEIGHT = 5

class TtfFont(object):
  def __init__(self, fontfile, text, height, font_height):
    self.text = text
    if font_height:
      self.font = ImageFont.truetype(fontfile, font_height)
      self.size = font.getsize(text)
    else:
      new_height = height
      while True:
        if new_height < MIN_FONT_HEIGHT:
          raise ValueError("Can't create font %s, height %s" % (fontfile, height))
        self.font = ImageFont.truetype(fontfile, new_height)
        self.size = self.font.getsize(text)
        if height >= self.size[1]:
          break
        else:
          new_height -= 1
    self.offset = tuple(-i for i in self.font.getoffset(text))

  def draw(self, drawable):
    drawable.text(self.offset, text=self.text, font=self.font)
