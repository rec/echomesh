from __future__ import absolute_import, division, print_function, unicode_literals

from PIL import Image

def make_image(x, mode='F'):
  try:
    x.size
  except:
    x = Image.open(x, 'r')
  return x
