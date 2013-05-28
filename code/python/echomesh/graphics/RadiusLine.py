from __future__ import absolute_import, division, print_function, unicode_literals

import math

def radius_line(angle, width, height):
  angle = angle % 360.0 - 180
  theta = math.radians(angle)

  h = height / 2.0
  w = width / 2.0
  t = math.tan(theta)

  tw = t * w
  if abs(tw) <= h:
    x, y = w, tw
  else:
    x, y = h / t, h

  begin = [-x + w, y + h]
  end = [x + w, -y + h]

  if -45 <= angle <= 135:
    return [end, begin]
  else:
    return [begin, end]
