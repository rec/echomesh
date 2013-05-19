from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.pattern import MakerFunctions
from echomesh.util import Call
from echomesh.pattern import PatternDesc

class Maker(object):
  def __init__(self, pattern_desc, function, *attributes):
    self.name = str(pattern_desc)
    self.table = PatternDesc.make_table(pattern_desc, attributes)
    self.function = function
    self.patterns = PatternDesc.make_patterns_from_desc(pattern_desc)

  def evaluate(self):
    return self()

  def __call__(self):
    # print('!!!!', self.table)
    table = dict((k, Call.call(v)) for k, v in self.table.iteritems())
    if self.patterns:
      arg = [[p() for p in self.patterns]]
    else:
      arg = []

    try:
      return self.function(*arg, **table)
    except Exception as e:
      if PatternDesc.RAISE_ORIGINAL_EXCEPTION:
        raise
      raise Exception('%s in %s' % (e, self.name))


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
  return Maker(pattern_desc, MakerFunctions.spread, 'steps')

def transpose(pattern_desc):
  return Maker(pattern_desc, MakerFunctions.transpose,
               'x', 'y', 'reverse_x', 'reverse_y')
_REGISTRY = PatternDesc.REGISTRY

_REGISTRY.register(choose)
_REGISTRY.register(concatenate)
_REGISTRY.register(inject)
_REGISTRY.register(insert)
_REGISTRY.register(reverse)
_REGISTRY.register(spread)
_REGISTRY.register(transpose)
