from __future__ import absolute_import, division, print_function, unicode_literals

from PIL import Image

def resize(image, x, y, stretch=False, top=None, left=None, mode='RGB'):
  size = x, y
  if stretch:
    return image.resize(size, resample=Image.ANTIALIAS)
  result = Image.new(mode, size)

  ratios = [d1 / d2 for d1, d2 in zip(size, image.size)]
  if ratios[0] < ratios[1]:
    new_size = (size[0], int(image.size[1] * ratios[0]))
  else:
    new_size = (int(image.size[0] * ratios[1]), size[1])

  image = image.resize(new_size, resample=Image.ANTIALIAS)
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
