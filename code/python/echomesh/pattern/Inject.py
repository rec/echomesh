from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.pattern.Pattern import Pattern

class Inject(Pattern):
  SETTINGS = {'mapping': {'default': {}}}
  PATTERN_COUNT = 1

  def _evaluate(self):
    pattern = self.patterns()[0]
    def _map(i):
      x = get('mapping').get(i)
      return x is not None and pattern[x]

    return [_map(i) for i in range(max(int(length), 0))]

