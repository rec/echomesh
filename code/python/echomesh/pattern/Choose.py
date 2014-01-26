from __future__ import absolute_import, division, print_function, unicode_literals

import itertools

from echomesh.pattern.Maker import maker
from echomesh.pattern.Pattern import Pattern

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

class Choose(Pattern):
  VARIABLES = 'choose',

  def _evaluate(self):
    length = len(self._patterns)
    def restrict(size):
      return int(max(0, min(length - 1, size)))

    if hasattr(choose, '__call__'):
      # TODO: there's no way to specify callables to choose so this case is
      # never called.
      zipped = itertools.izip_longest(*self.patterns())
      return [vec[restrict(choose(i))] for i, vec in enumerate(zipped)]
    else:
      return self._patterns[restrict(choose.evaluate())].evaluate()

