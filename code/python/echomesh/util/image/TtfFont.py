from __future__ import absolute_import, division, print_function, unicode_literals

from PIL import Image, ImageDraw, ImageFont

MIN_FONT_HEIGHT = 5

def draw_ttf(fontfile, text, height, font_height):
  if font_height:
    font = ImageFont.truetype(fontfile, font_height)
    size = font.getsize(text)
  else:
    new_height = height
    while True:
      if new_height < MIN_FONT_HEIGHT:
        raise ValueError("Can't create font %s, height %s" % (fontfile, height))
      font = ImageFont.truetype(fontfile, new_height)
      size = font.getsize(text)
      if height >= size[1]:
        break
      else:
        new_height -= 1
  offset = tuple(-i for i in font.getoffset(text))
  image = Image.new('RGBA', size)
  draw = ImageDraw.Draw(image)
  draw.text(offset, text=text, font=font)
  return image, size[0]
