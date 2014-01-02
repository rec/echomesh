from __future__ import absolute_import, division, print_function, unicode_literals

import cechomesh

from echomesh.color import ColorConv
from echomesh.util import Importer
from cechomesh import Transform

numpy = Importer.imp('numpy')

def color_spread(begin, end, steps=2, transform=None, use_hsb=True):
  return cechomesh.color_spread(colors=[begin, end],
                                model='hsb' if use_hsb else 'rgb',
                                max_steps=steps,
                                transform=transform)
