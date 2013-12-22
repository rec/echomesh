from __future__ import absolute_import, division, print_function, unicode_literals

from cechomesh import to_color

from echomesh.color import ColorConv
from echomesh.util import Importer
from echomesh.expression import Transform

numpy = Importer.imp('numpy')

def color_spread(begin, end, steps, transform=None, use_hsv=True):
  if use_hsv:
    colors = ColorConv.rgb_to_hsv([begin, end]).T
  else:
    colors = numpy.array([begin, end]).T
  steps = int(steps)
  if transform:
    fn, fi = transform
    step_array = [fi(numpy.linspace(fn(s), fn(f), steps)) for s, f in colors]
  else:
    step_array = [numpy.linspace(s, f, steps) for s, f in colors]
  if use_hsv:
    step_array = ColorConv.hsv_to_rgb(numpy.array(step_array).T)
  else:
    step_array = numpy.array(step_array).T
  return step_array

def color_name_spread(begin=None, end=None, steps=None, transform=None):
  transform = transform or Transform.transform(transform)

  # TODO: disallow these defaults?
  return color_spread(to_color(begin or 'black'),
                      to_color(end or 'white'),
                      steps or 2, transform=transform)
