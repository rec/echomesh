from __future__ import absolute_import, division, print_function, unicode_literals

import cechomesh

from echomesh.base import Config

@maker('steps', 'total_steps')
def spread(colors=None, hsv=True, steps=None, total_steps=None, transform=None):
  return cechomesh.spread(
    colors,
    hsv,
    Config.get('light', 'count'),
    steps and steps.evaluate(),
    total_steps and total_steps.evaluate(),
    transform)
