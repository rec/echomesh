from __future__ import absolute_import, division, print_function, unicode_literals

import collections
import six

from echomesh.expression import Expression
from echomesh.util.registry import Registry

REGISTRY = Registry.Registry('pattern types')

RAISE_ORIGINAL_EXCEPTION = not False

_Parent = collections.namedtuple('_PatternDesc', 'element description name')

class _PatternDesc(_Parent):
  def __str__(self):
    return 'pattern "%s" in element "%s"' % (
      self.name, self.element.class_name())

def _make_pattern(desc, is_top_level):
  type_value = desc.description.pop('type', None)
  if not type_value:
    raise Exception('No type value found')
  entry = REGISTRY.entry(type_value)
  if not entry:
    raise Exception('Didn\'t understand type="%s"' % type_value)

  if not is_top_level:
    desc = _PatternDesc(desc.element, desc.description,
                        desc.name + ':%s' % entry.name)
  return entry.function(desc)

def make_patterns_for_element(element, description):
  result = {}
  for name, desc in six.iteritems(description):
    result[name] = _make_pattern(_PatternDesc(element, desc, name), True)
  return result

def make_table_and_patterns(pattern_desc, attributes):
  table = {}
  patterns = []

  desc = pattern_desc.description
  pd = pattern_desc

  try:
    for k, v in six.iteritems(desc):
      if not k.startswith('pattern'):
        if k in attributes:
          v = Expression.expression(v, pattern_desc.element)
        table[k] = v

    pats = desc.get('patterns') or desc.get('pattern') or []
    if type(pats) is not list:
      pats = [pats]

    for p in pats:
      pd = _PatternDesc(pattern_desc.element, p, pattern_desc.name)
      pattern = _make_pattern(pd, False)
      if pattern:
        patterns.append(pattern)
  except Exception as e:
    if RAISE_ORIGINAL_EXCEPTION:
      raise
    else:
      raise Exception('%s in %s' % (e, pd))

  return table, patterns
