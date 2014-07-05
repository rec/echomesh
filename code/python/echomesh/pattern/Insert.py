from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.Cechomesh import cechomesh

from echomesh.base import Settings
from echomesh.color.LightCount import light_count
from echomesh.pattern.Pattern import Pattern

class Insert(Pattern):
  PATTERN_COUNT = 1

  HELP = """Inserts a given pattern into a larger ColorList."""

  SETTINGS = {
	  'length': {  # TODO: this can be omitted if rollover is False.
      'default': 0,
      'help': 'The total number of lights in the output ColorList.',
      },
    'offset': {
      'default': 0,
      'help': ('The starting offset of the input pattern within the output.'
               'offset can be negative.'),
      },
    'rollover': {
      'default': False,
      'help': 'If true, the input pattern rolls over to the start of the output',
      },
    'skip': {
      'default': 1,
      'help': 'How many lights to skip when inserting.  skip can be negative.',
      },
    }

  def _evaluate(self):
    color_lists = self.patterns()
    assert len(color_lists) == 1
    color_list = color_lists[0]

    skip = int(self.get('skip'))
    offset = int(self.get('offset'))
    length = self.get('length') or light_count(Settings.get)
    rollover = bool(self.get('rollover'))

    return cechomesh.insert_color_list(color_list, offset, length, rollover, skip)
