from __future__ import absolute_import, division, print_function, unicode_literals

import six

from PIL import Image

from echomesh.util.image.Crop import crop

def resize(image, x, y, stretch=False, top=None, left=None, mode='RGB',
           top_offset=0, left_offset=0, bottom_offset=0, right_offset=0,
           resample=None):
    if x <= 0:
        raise ValueError('x must be greater than zero')
    if y <= 0:
        raise ValueError('y must be greater than zero')
    if resample:
        try:
            resample = getattr(Image, resample.upper())
        except:
            raise ValueError("Didn't understand resample=%s" % resample)
    else:
        resample = Image.ANTIALIAS
    image = crop(image, top_offset, left_offset, bottom_offset, right_offset)

    size = x, y
    if stretch:
        return image.resize(size, resample=resample)
    result = Image.new(mode, size)

    ratios = [d1 / d2 for d1, d2 in zip(size, image.size)]
    if ratios[0] < ratios[1]:
        new_size = (size[0], int(image.size[1] * ratios[0]))
    else:
        new_size = (int(image.size[0] * ratios[1]), size[1])

    image = image.resize(new_size, resample=resample)
    if left is None:
        box_x = int((x - new_size[0]) / 2)
    elif left:
        box_x = 0
    else:
        box_x = x - new_size[0]

    if top is None:
        box_y = int((y - new_size[1]) / 2)
    elif top:
        box_y = 0
    else:
        box_y = y - new_size[1]

    result.paste(image, box=(box_x, box_y))
    return result
