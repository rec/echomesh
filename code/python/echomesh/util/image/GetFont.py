from __future__ import absolute_import, division, print_function, unicode_literals

import os.path

from echomesh.util.image import PcfFont, TtfFont

INFINITY = float('inf')

_FONT_HANDLERS = {
  '.pcf': PcfFont.PcfFont,
  '.ttf': TtfFont.TtfFont,
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
