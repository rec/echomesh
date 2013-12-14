from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.pattern.Maker import maker

# The Python built-in works perfectly.
@maker
def reverse(light_sets):
  assert len(light_sets) == 1
  light_set = light_sets[0]
  return reversed(light_set)
