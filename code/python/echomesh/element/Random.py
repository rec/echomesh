from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util.thread import TimeLoop
from echomesh.util.math import Poisson

DEFAULT_INTERVAL = 10.0

class Random(TimeLoop.TimeLoop):
  def __init__(self, parent, element):
    super(Random, self).__init__(name='RandomCommand')
    self.mean = element.get('data', {}).get('mean', DEFAULT_INTERVAL)
    self.command = element.get('command', {})
    assert self.command['function']

  def _next_time(self, t):
    return t + Poisson.next_poisson(self.mean)

  def _command(self, t):
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
