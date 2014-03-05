from __future__ import absolute_import, division, print_function, unicode_literals

import os.path

from PIL import ImageFont

_SUFFIX = '.ttf'

def _get_font(fontfile, height, text):
  try:
    font = ImageFont.truetype(fontfile, height)
  except:
    raise Exception('Can\'t open font file %s' % fontfile)
  return font, font.getsize(text)

def get_font(fontfile, text, height, font_height=0):
  if not fontfile.endswith(_SUFFIX):
    fontfile += _SUFFIX

  if not os.path.isabs(fontfile):
    fontfile = os.path.join('asset', 'font', fontfile)

  if font_height:
    return _get_font(fontfile, font_height, text)

  new_height = height
  while True:
    font, size = _get_font(fontfile, new_height, text)
    if height >= size[1]:
      return font, size
    else:
      new_height -= 1

