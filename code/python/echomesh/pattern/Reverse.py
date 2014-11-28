from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.pattern.Pattern import Pattern

class Reverse(Pattern):
    HELP = """Reverses patterns that are fed to it."""

    PATTERN_COUNT = 1

    def _evaluate(self):
        return reversed(self.patterns()[0])
