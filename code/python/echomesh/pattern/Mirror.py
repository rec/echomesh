from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.Cechomesh import cechomesh

from echomesh.base import Settings
from echomesh.pattern.Pattern import Pattern

class Mirror(Pattern):
    HELP = """Create the mirror image of an x, y pattern."""

    SETTINGS = {
      'columns': {
        'default': 0,
        'help': ('The number of columns in the original pattern. Unnecessary '
                 'for patterns which already have columns.'),
        },
      'rows': {
        'default': 0,
        'help': ('The number of rows in the original pattern. Unnecessary '
                 'for patterns which already have columns.'),
        },
      'reverse_x': {
        'default': False,
        'help': 'Do we mirror image around the x axis?',
        },
      'reverse_y': {
        'default': False,
        'help': 'Do we mirror image around the y axis?',
        },
      }

    PATTERN_COUNT = 1

    def _evaluate(self):
        color_lists = self.patterns()
        assert len(color_lists) == 1
        color_list = color_lists[0]

        columns = self.get('columns') or getattr(color_list, 'columns', 0)
        rows = self.get('rows')

        if rows:
            columns = columns or cechomesh.compute_rows(len(color_list), rows)
        elif columns:
            rows = cechomesh.compute_rows(len(color_list), columns)
        else:
            columns, rows = Settings.get('light', 'visualizer', 'layout')

        return cechomesh.mirror_color_list(
          color_list, int(columns), int(rows),
          bool(self.get('reverse_x')), bool(self.get('reverse_y')))
