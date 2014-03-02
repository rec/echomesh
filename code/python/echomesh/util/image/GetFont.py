from __future__ import absolute_import, division, print_function, unicode_literals

import os.path

from PIL import ImageFont

_SUFFIX = '.ttf'

def get_font(fontfile, text, height):
  if not fontfile.endswith(_SUFFIX):
    fontfile += _SUFFIX
  if not os.path.isabs(fontfile):
    fontfile = os.path.join('asset', 'font', fontfile)

  new_height = height
  while True:
    try:
      font = ImageFont.truetype(fontfile, new_height)
    except:
      raise Exception('Can\'t open font file %s' % fontfile)
    size = font.getsize(text)
    if height >= size[1]:
      return font, size
    else:
      new_height -= 1

