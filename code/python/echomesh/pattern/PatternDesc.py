from __future__ import absolute_import, division, print_function, unicode_literals

import collections

from echomesh.expression.Expression import Expression
from echomesh.util import Registry

REGISTRY = Registry.Registry('pattern types')

RAISE_ORIGINAL_EXCEPTION = not False

_Parent = collections.namedtuple('_PatternDesc', 'element description name')

class _PatternDesc(_Parent):
  def __str__(self):
    return 'pattern "%s" in element "%s"' % (
      self.name, self.element.class_name())

def _make_one_pattern(desc, is_top_level):
  type_value = desc.description.pop('type', None)
  if not type_value:
    raise Exception('No type value found')
  full_type, maker = REGISTRY.get_key_and_value_or_none(type_value)
  if not full_type:
    raise Exception('Didn\'t understand type="%s"' % type_value)

  if not is_top_level:
    desc = _PatternDesc(desc.element, desc.description,
                       desc.name + ':%s' % full_type)
  return maker(desc)

def make_patterns_for_element(element, description):
  result = {}
  for name, desc in description.iteritems():
    result[name] = _make_one_pattern(_PatternDesc(element, desc, name), True)
  return result

def make_table(pattern_desc, attributes):
  table = {}
  for k, v in pattern_desc.description.iteritems():
    if k.startswith('pattern'):
      continue
    if k in attributes:
      try:
        v = Expression(v, pattern_desc.element)
      except Exception as e:
        if RAISE_ORIGINAL_EXCEPTION:
          raise
        raise Exception('%s in %s' % (e, pattern_desc))

    table[k] = v
  return table

def make_patterns_from_desc(pattern_desc):
  desc = pattern_desc.description
  patterns = desc.get('patterns') or desc.get('pattern') or []
  if type(patterns) is not list:
    patterns = [patterns]

  result = []

  for p in patterns:
    pd = _PatternDesc(pattern_desc.element, p, pattern_desc.name)
    try:
      pattern = _make_one_pattern(pd, False)
    except Exception as e:
      if RAISE_ORIGINAL_EXCEPTION:
        raise
      raise Exception('%s in %s' % (e, pd))
    else:
      if pattern:
        result.append(pattern)
  return result

