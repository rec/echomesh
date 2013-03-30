from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.color import ColorConv
from echomesh.color import ColorTable
from echomesh.util import Importer
from echomesh.expression import Transform

numpy = Importer.imp('numpy')

def color_spread(begin, end, steps, transform=None, use_hsv=True):
  if use_hsv:
    colors = ColorConv.rgb_to_hsv([begin, end]).T
  else:
    colors = numpy.array([begin, end]).T
  if transform:
    fn, fi = transform
    steps = [fi(numpy.linspace(fn(s), fn(f), steps)) for s, f in colors]
  else:
    steps = [numpy.linspace(s, f, steps) for s, f in colors]
  if use_hsv:
    steps = ColorConv.hsv_to_rgb(numpy.array(steps).T)
  else:
    steps = numpy.array(steps).T
  return steps

def color_name_spread(begin=None, end=None, steps=None, transform=None):
  if transform:
    transform = Transform.transform(transform)

  # TODO: disallow these defaults?
  return color_spread(ColorTable.to_color(begin or 'black'),
                      ColorTable.to_color(end or 'white'),
                      steps or 2, transform=transform)
