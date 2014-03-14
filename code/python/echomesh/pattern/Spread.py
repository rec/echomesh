from __future__ import absolute_import, division, print_function, unicode_literals

import cechomesh
import six

from echomesh.base import Config
from echomesh.color.LightCount import light_count
from echomesh.pattern.Pattern import Pattern
from echomesh.util.string.Plural import plural

class Spread(Pattern):
  SETTINGS = {
    'colors': {
      'default': [],
      'constant': True,
      'help': '',
      },
    'model': {
      'default': None,
      'constant': True,
      'help': '',
      },
    'transform': {
      'default': None,
      'constant': True,
      'help': '',
      },
    'steps': {
      'default': None,
      'constant': True,
      'help': '',
      },
    'total_steps': {
      'default': None,
      'constant': True,
      'help': '',
      },
    }
  PATTERN_COUNT = 0

  def _evaluate(self):
    colors, error_colors = cechomesh.color_list_with_errors(self.get('colors'))
    if error_colors:
      raise Exception('\nCan\'t understand %s: %s.' % (
          plural(len(error_colors), 'color'), ', '.join(error_colors)))

    steps = self.get('steps')
    total_steps = self.get('total_steps')
    if total_steps is None:
      if steps is None:
        total_steps = None
      else:
        total_steps = steps
        steps = None

    return cechomesh.color_spread(
      colors,
      self.get('model'),
      max_steps=light_count(Config.get),
      steps=steps,
      total_steps=total_steps,
      transform=self.get('transform'))
