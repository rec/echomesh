from __future__ import absolute_import, division, print_function, unicode_literals

def crop(image, top_offset=0, left_offset=0, bottom_offset=0, right_offset=0):
  if bottom_offset or top_offset or left_offset or right_offset:
    width, height = image.size
    image = image.crop(box=(left_offset, top_offset,
                            width - right_offset, height - left_offset))
  return image

