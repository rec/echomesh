from __future__ import absolute_import, division, print_function, unicode_literals

import collections

from echomesh.base import DataFile
from echomesh.base import GetPrefix
from echomesh.expression import Expression
from echomesh.pattern import REGISTRY

RAISE_ORIGINAL_EXCEPTION = not False

_Parent = collections.namedtuple('_PatternDesc', 'element description name')

class _PatternDesc(_Parent):
  def __str__(self):
    return 'pattern "%s" in element "%s"' % (
      self.name, self.element.class_name())


def _make_pattern(element, description, name, is_top_level):
  entry = REGISTRY.get_by_type(description)
  if is_top_level:
    name += ':%s' % entry.name

  return entry.function(_PatternDesc(element, description, name))

def make_patterns_for_element(element, description):
  result = {}
  for name, desc in description.items():
    result[name] = _make_pattern(element, desc, name, True)
  return result

def make_table_and_patterns(pattern_desc, attributes):
  pd = pattern_desc
  table = {}
  patterns = []

  desc = pd.description

  for k, v in desc.items():
    if not k.startswith('pattern'):
      if k in attributes:
        v = Expression.expression(v, pd.element)
      table[k] = v

  pats = desc.get('patterns') or desc.get('pattern') or []
  if type(pats) is not list:
    pats = [pats]

  return table, [_make_pattern(pd.element, p, pd.name, False) for p in pats]

def make_pattern_from_file(element, name):
  desc = DataFile.load('pattern', name)[0]
  return _make_pattern(element, desc, name, True)
