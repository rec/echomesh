from __future__ import absolute_import, division, print_function, unicode_literals

from PIL import Image

def make_image(x, mode='RGB'):
    try:
        x.size
    except:
        x = Image.open(x, mode='r')
    if x.mode != mode:
        x = x.convert(mode=mode)
    return x
