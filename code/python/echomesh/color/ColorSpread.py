from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.color import ColorConv
from echomesh.color import ColorTable
from echomesh.util import Importer
from echomesh.expression import Transform

numpy = Importer.imp('numpy')

def color_spread(begin, end, points, transform=None, use_hsv=True):
  if use_hsv:
    colors = ColorConv.rgb_to_hsv([begin, end]).T
  else:
    colors = numpy.array([begin, end]).T
  if transform:
    fn, fi = transform
    points = [fi(numpy.linspace(fn(s), fn(f), points)) for s, f in colors]
  else:
    points = [numpy.linspace(s, f, points) for s, f in colors]
  if use_hsv:
    points = ColorConv.hsv_to_rgb(numpy.array(points).T)
  else:
    points = numpy.array(points).T
  return points

def color_name_spread(begin=None, end=None, points=None, transform=None):
  if transform:
    transform = Transform.transform(transform)

  # TODO: disallow these defaults?
  return color_spread(ColorTable.to_color(begin or 'black'),
                      ColorTable.to_color(end or 'white'),
                      points or 2, transform=transform)
