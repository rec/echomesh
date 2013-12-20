from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.pattern.Maker import maker

@maker
def inject(light_sets, mapping, length):
  """
    mapping:
      Maps a light index in the result to the light index in the original
      light_set.  We need a reverse mapping because we need a way to map one
      light in the input to many lights in the output.

  """
  assert len(light_sets) == 1
  light_set = light_sets[0]

  def _map(i):
    x = mapping.get(i)
    return x is not None and light_set[x]

  return [_map(i) for i in range(max(int(length), 0))]