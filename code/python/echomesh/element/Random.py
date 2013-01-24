from __future__ import absolute_import, division, print_function, unicode_literals

import bisect
import random

from echomesh.element import Loop
from echomesh.util.math import Poisson
from echomesh.element import Register

DEFAULT_INTERVAL = 10.0

class Random(Loop.Loop):
  def __init__(self, parent, description):
    super(Random, self).__init__(parent, description, name='Random')

  def _next_time(self, t):
    return t + Poisson.next_poisson(self.mean)

  def _loop(self, t):
    self.execute_command(self.command)


def select_random(score, event, *choices):
  if choices:
    item = random.choice(choices)
    function_name = item.get('function', None)
    function = score.functions.get(function_name, None)
    if function:
      keywords = item.get('keywords', {})
      arguments = item.get('arguments', [])
      function(score, event, *arguments, **keywords)
    else:
      LOGGER.error('No function named "%s": %s, %s', function_name, item, choices)
  else:
    LOGGER.error('No arguments to select_random')

Register.register(Random)
