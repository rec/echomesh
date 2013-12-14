from __future__ import absolute_import, division, print_function, unicode_literals

import itertools

from echomesh.pattern.Maker import maker

@maker('choose')
def choose(light_sets, choose=None):
  length = len(light_sets)
  def restrict(size):
    return int(max(0, min(length - 1, size)))

  if hasattr(choose, '__call__'):
    # TODO: there's no way to specify callables to choose.
    zipped = itertools.izip_longest(*light_sets)
    return [vec[restrict(choose(i))] for i, vec in enumerate(zipped)]
  else:
    return light_sets[restrict(choose.evaluate())]
