from __future__ import absolute_import, division, print_function, unicode_literals

import cechomesh
import six

from echomesh.base import Config
from echomesh.pattern.Maker import maker

@maker('steps', 'total_steps')
def spread(colors=None, model='hsb', steps=None, transform=None):
  steps = steps and steps.evaluate()
  if isinstance(steps, six.integer_types):
    total_steps = steps
    steps = None
  else:
    total_steps = None
  return cechomesh.color_spread(
    colors,
    model,
    max_steps=Config.get('light', 'count'),
    steps=steps,
    total_steps=total_steps,
    transform=transform)
