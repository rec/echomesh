from __future__ import absolute_import, division, print_function, unicode_literals

import cechomesh
import six

from echomesh.base import Config
from echomesh.pattern.Maker import maker
from echomesh.util import Log
from echomesh.util.string.Plural import plural

LOGGER = Log.logger(__name__)

@maker('steps', 'total_steps')
def spread(colors=None, model='hsb', steps=None, transform=None):
  colors, error_colors = cechomesh.color_list_with_errors(colors)
  if error_colors:
    raise Exception('\nCan\'t understand %s: %s.' % (
        plural(len(error_colors), 'color'), ', '.join(error_colors)))

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
