from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.color import ColorConv
from echomesh.util import Importer

numpy = Importer.imp('numpy')

def color_spread(start, finish, points, transform=None):
  hsv = ColorConv.rgb_to_hsv([start, finish])
  if transform:
    fn, fi = transform
    points = [fi(numpy.linspace(fn(s), fn(f), points)) for s, f in hsv.T]
  else:
    points = [numpy.linspace(s, f, points) for s, f in hsv.T]
  return ColorConv.hsv_to_rgb(numpy.array(points).T)
