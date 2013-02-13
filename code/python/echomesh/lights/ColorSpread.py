from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.lights import ColorConv
from echomesh.util import Importer

numpy = Importer.imp('numpy')

def color_spread(start, finish, points):
  hsv = ColorConv.rgb_to_hsv([start, finish])
  return ColorConv.hsv_to_rgb(numpy.array([numpy.linspace(s, f, points) for s, f in hsv.T]).T)
