from __future__ import absolute_import, division, print_function, unicode_literals

import cechomesh

from echomesh.color import ColorConv
from cechomesh import Transform

def color_spread(begin, end, steps, transform=None, use_hsb=True):
  return cechomesh.color_spread([begin, end],
                                'hsb' if use_hsb else 'rgb',
                                max_steps=steps,
                                transform=transform)
