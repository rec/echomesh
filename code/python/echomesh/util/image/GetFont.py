from __future__ import absolute_import, division, print_function, unicode_literals

import os.path

from PIL import ImageFont

def get_font(fontfile, text, height):
  new_height = height
  while True:
    try:
      if not os.path.isabs(fontfile):
        fontfile = os.path.join('asset', 'font', fontfile)
      font = ImageFont.truetype(fontfile, new_height)
    except:
      raise Exception('Can\'t open font file %s' % fontfile)
    size = font.getsize(text)
    if height >= size[1]:
      return font, size
    else:
      new_height -= 1

