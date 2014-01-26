from __future__ import absolute_import, division, print_function, unicode_literals

import itertools

from echomesh.pattern.Pattern import Pattern

class Choose(Pattern):
  VARIABLES = 'choose',

  def _evaluate(self):
    length = len(self._patterns)
    def restrict(size):
      return int(max(0, min(length - 1, size)))
    choose = self.get('choose')
    if hasattr(choose, '__call__'):
      # TODO: there's no way to specify callables to choose so this case is
      # never called.
      zipped = itertools.izip_longest(*self.patterns())
      return [vec[restrict(choose(i))] for i, vec in enumerate(zipped)]
    else:
      return self._patterns[restrict(choose)].evaluate()

