from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh import cechomesh

from echomesh.base import Config
from echomesh.pattern.Pattern import Pattern

class Column(Pattern):
  HELP = 'Set or rest the number of columns in an x, y pattern.'

  SETTINGS = {
    'columns': {
      'help': 'The new number of columns',
      },
    }

  PATTERN_COUNT = 1

  def _evaluate(self):
    return cechomesh.ColorList(self.patterns()[0], self.get('columns'))
