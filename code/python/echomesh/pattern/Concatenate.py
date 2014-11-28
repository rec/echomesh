from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.Cechomesh import cechomesh

from echomesh.pattern.Pattern import Pattern

class Concatenate(Pattern):
    HELP = """Concatenates multiple patterns end-to-end."""

    def _evaluate(self):
        return cechomesh.concatenate_color_lists(self.patterns())
