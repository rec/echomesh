from __future__ import absolute_import, division, print_function, unicode_literals

import collections

from echomesh.expression.Expression import Expression
from echomesh.pattern import MakerFunctions
from echomesh.util import Call
from echomesh.util import Registry

_REGISTRY = Registry.Registry('pattern types')

class PatternDesc(collections.namedtuple('PatternDesc',
                                         'element description name')):
  def __str__(self):
    return 'pattern "%s" in element "%s"' % (
      self.name, self.element.class_name())

def _make_pattern(desc, is_top_level):
  type_value = desc.description.pop('type', None)
  if not type_value:
    raise Exception('No type value found')
  full_type, maker = _REGISTRY.get_key_and_value_or_none(type_value)
  if not full_type:
    raise Exception('Didn\'t understand type="%s"' % type_value)

  if not is_top_level:
    desc = PatternDesc(desc.element, desc.description,
                       desc.name + ':%s' % full_type)
  return maker(desc)

def make_patterns(element, description):
  result = {}
  for name, desc in description.iteritems():
    result[name] = _make_pattern(PatternDesc(element, desc, name), True)
  return result

class Maker(object):
  def __init__(self, pattern_desc, function, *attributes):
    self.pattern_desc = pattern_desc
    self.table = {}
    desc = pattern_desc.description
    for k, v in desc.iteritems():
      if k.startswith('pattern'):
        continue
      if k in attributes:
        v = Expression(v, pattern_desc.element)
      self.table[k] = v
    self.function = function
    patterns = desc.get('patterns') or desc.get('pattern') or []
    self.patterns = []
    if type(patterns) is not list:
      patterns = [patterns]

    for p in patterns:
      pd = PatternDesc(pattern_desc.element, p, pattern_desc.name)
      try:
        pattern = _make_pattern(pd, False)
      except Exception as e:
        raise Exception('%s in %s' % (e, pd))
      else:
        if pattern:
          self.patterns.append(pattern)

  def evaluate(self):
    return self()

  def __call__(self):
    table = dict((k, Call.call(v)) for k, v in self.table.iteritems())
    if self.patterns:
      arg = [[p() for p in self.patterns]]
    else:
      arg = []

    try:
      return self.function(*arg, **table)
    except Exception as e:
      raise Exception('%s in %s' % (e, self.pattern_desc))


  def is_constant(self):
    return all(v.is_constant() for v in self.table.itervalues())

def choose(pattern_desc):
  return Maker(pattern_desc, MakerFunctions.choose, 'choose')

def concatenate(pattern_desc):
  return Maker(pattern_desc, MakerFunctions.concatenate)

def inject(pattern_desc):
  return Maker(pattern_desc, MakerFunctions.inject)

def insert(pattern_desc):
  return Maker(pattern_desc, MakerFunctions.insert,
               'begin', 'length', 'rollover', 'skip')

def reverse(pattern_desc):
  return Maker(pattern_desc, MakerFunctions.reverse)

def spread(pattern_desc):
  return Maker(pattern_desc, MakerFunctions.spread, 'colors', 'steps')

def transpose(pattern_desc):
  return Maker(pattern_desc, MakerFunctions.transpose,
               'x', 'y', 'reverse_x', 'reverse_y')

_REGISTRY.register(choose)
_REGISTRY.register(concatenate)
_REGISTRY.register(inject)
_REGISTRY.register(insert)
_REGISTRY.register(reverse)
_REGISTRY.register(spread)
_REGISTRY.register(transpose)
