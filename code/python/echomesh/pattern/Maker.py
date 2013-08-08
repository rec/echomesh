from __future__ import absolute_import, division, print_function, unicode_literals

import six

from echomesh.util import Call
from echomesh.pattern import PatternDesc

class Maker(object):
  def __init__(self, pattern_desc, function, *attributes):
    self.name = str(pattern_desc)
    self.function = function
    self.table, self.patterns = PatternDesc.make_table_and_patterns(
      pattern_desc, attributes)

  def evaluate(self):
    table = dict((k, Call.call(v)) for k, v in six.iteritems(self.table))
    if self.patterns:
      arg = [[p.evaluate() for p in self.patterns]]
    else:
      arg = []

    try:
      return self.function(*arg, **table)
    except Exception as e:
      if PatternDesc.RAISE_ORIGINAL_EXCEPTION:
        raise
      raise Exception('%s in %s' % (e, self.name))

  def is_constant(self):
    return all(v.is_constant() for v in six.itervalues(self.table))

def maker(*a):
  args = a
  def wrap(f):
    def wrapped(pattern_desc):
      return Maker(pattern_desc, f, *args)
    return wrapped

  if len(args) == 1 and hasattr(args[0], '__call__'):
    args = ()
    return wrap(a[0])
  else:
    return wrap

