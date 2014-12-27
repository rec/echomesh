from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.Cechomesh import cechomesh

import itertools

from echomesh.pattern.Pattern import Pattern
from echomesh.util.string.Plural import plural

class List(Pattern):
    HELP = 'Display a spread of colors between two or more color endpoints.'
    CONSTANT = True
    PATTERN_COUNT = 0

    SETTINGS = {
      'colors': {
        'default': [],
        'help': 'A list of colors to be displayed.',
        },
      'columns': {
        'default': 0,
        'help': 'The number of columns in the result',
        },
      }

    PATTERN_COUNT = 0

    def _evaluate(self):
        colors = self.get_raw('colors')
        has_lists, has_scalars = False, False
        for c in colors:
            is_list = isinstance(c, list)
            has_lists = has_lists or is_list
            has_scalars = has_scalars or not is_list

        if has_scalars:
            if has_lists:
                raise Exception('Can\'t mix lists and scalars in pattern.List')
            colors = [colors]
        max_column = max(len(c) for c in colors)
        columns = self.get('columns') or max_column
        if not max_column:
            # Empty list.
            return cechomesh.Colorlist(columns=columns)

        ce = (cechomesh.color_list_with_errors(c) for c in colors)
        color_lists, errors = zip(*ce)
        errors = list(itertools.chain(*errors))
        if errors:
            raise Exception('\nCan\'t understand %s: %s.' % (
                plural(len(errors), 'color'), ', '.join(errors)))
        result = cechomesh.ColorList(columns=columns)
        for i, cl in enumerate(color_lists):
            cl.size = columns
            result.extend(cl)
        return result
