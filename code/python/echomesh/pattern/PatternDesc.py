from __future__ import absolute_import, division, print_function, unicode_literals

from collections import namedtuple

from echomesh.base import DataFile
from echomesh.base import GetPrefix
from echomesh.expression import Expression
from echomesh.pattern import REGISTRY

RAISE_ORIGINAL_EXCEPTION = True

class PatternDesc(namedtuple('PatternDesc', 'element description name')):
  def __str__(self):
    return 'pattern "%s" in element "%s"' % (
      self.name, self.element.class_name())


def make_pattern(element, name, description, is_top_level):
  entry = REGISTRY.get_from_description(description)
  if is_top_level:
    name = '%s:%s' % (name, entry.name)

  return entry.function(PatternDesc(element, description, name))

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

  return table, [make_pattern(pd.element, pd.name, p, False) for p in pats]

def make_pattern_from_file(element, name):
  desc = DataFile.load('pattern', name)[0]
  return make_pattern(element, name, desc, True)
