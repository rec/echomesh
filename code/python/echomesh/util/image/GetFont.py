from __future__ import absolute_import, division, print_function, unicode_literals

import os.path

from PIL import ImageFont, PcfFontFile

from echomesh.util import Log

LOGGER = Log.logger(__name__)
MIN_FONT_HEIGHT = 5

def _pcf_maker(fontfile, text, height, font_height):
  if height or font_height:
    LOGGER.warning("You can't set a height or font_height for .pcf fonts")
  with open(fontfile, 'rb') as f:
    font = PcfFontFile.PcfFontFile(f)
  return font

def _ttf_maker(fontfile, text, height, font_height):
  if font_height:
    return ImageFont.truetype(fontfile, font_height)
  new_height = height
  while True:
    if new_height < MIN_FONT_HEIGHT:
      raise ValueError("Can't create font %s of height %s" % (fontfile, height))
    font = ImageFont.truetype(fontfile, new_height)
    size = font.getsize(text)
    if height >= size[1]:
      return font
    else:
      new_height -= 1

_FONT_HANDLERS = {
  '.pcf': _pcf_maker,
  '.ttf': _ttf_maker,
  }

def _resolve_name(fontfile):
  if not os.path.isabs(fontfile):
    fontfile = os.path.join('asset', 'font', fontfile)

  extension = os.path.splitext(fontfile)[1][1:]
  if extension:
    if extension not in _FONT_HANDLERS:
      raise ValueError("Don't understand font type %s from file %s" %
                       (fontfile, extension))
    if not os.path.exists(fontfile):
      raise IOError("No such file: '%s'" % fontfile)
    return fontfile, extension

  for extension in _FONT_HANDLERS:
    name = fontfile + extension
    if os.path.exists(name):
      return name, extension
  raise IOError("No font named '%s'" % fontfile)


def get_font(fontfile, text, height=0, font_height=0):
  fontfile, extension = _resolve_name(fontfile)
  return _FONT_HANDLERS[extension](fontfile, text, height, font_height)
