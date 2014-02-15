from __future__ import absolute_import, division, print_function, unicode_literals

from PIL import Image

from echomesh.util.image.MakeImage import make_image

def resize_to(image, x, y, top=True, left=True, mode='RGB'):
  image = make_image(image)
  size = x, y
  ratios = [d1 / d2 for d1, d2 in zip(size, image.size)]
  if ratios[0] < ratios[1]:
    new_size = (size[0], int(image.size[1] * ratios[0]))
  else:
    new_size = (int(image.size[0] * ratios[1]), size[1])

  box = (0 if top else x - new_size[0], 0 if left else y - new_size[1])

  result = Image.new(mode, size)
  result.paste(image.resize(new_size), box=box)
  return result
