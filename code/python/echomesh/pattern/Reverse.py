from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.pattern.Maker import maker
from echomesh.pattern.Pattern import Pattern

# The Python built-in works perfectly.
@maker
def reverse(light_sets):
  assert len(light_sets) == 1
  light_set = light_sets[0]
  return reversed(light_set)

class Reverse(Pattern):
  def finish_initialization(self, desc):
    assert len(self.patterns) == 1, 'Reverse must contain exactly one pattern.'

  def _evaluate(self):
    return reverse(self.patterns[0].evaluate())
