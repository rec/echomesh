from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.pattern.Pattern import Pattern

class Inject(Pattern):
    HELP = """Injects a pattern into a larger ColorMatrix."""

    SETTINGS = {
      'mapping': {
        'default': {},
        'help': ('A mapping indicating for each position in the incoming '
                 ' pattern where the final color is mapped.'),
        },
      }

    PATTERN_COUNT = 1

    def _evaluate(self):
        pattern = self.patterns()[0]
        mapping = get('mapping')
        def _map(i):
            x = mapping.get(i)
            return x is not None and pattern[x]

        return [_map(i) for i in range(max(int(length), 0))]
