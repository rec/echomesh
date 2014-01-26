from __future__ import absolute_import, division, print_function, unicode_literals

import cechomesh
import six

from echomesh.base import Config
from echomesh.pattern.Pattern import Pattern
from echomesh.util.string.Plural import plural

class Spread(Pattern):
  CONSTANTS = 'colors',
  OPTIONAL_CONSTANTS = 'model', 'transform'
  OPTIONAL_VARIABLES = 'steps', 'total_steps'
  PATTERN_COUNT = 0

  def _evaluate(self):
    colors, error_colors = cechomesh.color_list_with_errors(self.get('colors'))
    if error_colors:
      raise Exception('\nCan\'t understand %s: %s.' % (
          plural(len(error_colors), 'color'), ', '.join(error_colors)))

    steps = self.get('steps')
    if isinstance(steps, six.integer_types):
      total_steps = steps
      steps = None
    else:
      total_steps = None

    return cechomesh.color_spread(
      colors,
      self.get('model'),
      max_steps=Config.get('light', 'count'),
      steps=steps,
      total_steps=total_steps,
      transform=self.get('transform'))
