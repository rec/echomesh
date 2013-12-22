from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.pattern import PatternDesc
from echomesh.util import Call
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class Maker(object):
  def __init__(self, pattern_desc, function, *attributes):
    self.name = str(pattern_desc)
    self.function = function
    self.table, self.patterns = PatternDesc.make_table_and_patterns(
      pattern_desc, attributes)
    self.attributes = attributes
    self.pattern_desc = pattern_desc

  def evaluate(self):
    table = dict((k, Call.call(v)) for k, v in self.table.items())
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
    is_constant = all(v.is_constant() for v in six.itervalues(self.table))
    return is_constant

  def __str__(self):
    return 'Maker(pattern_desc=%s, function=%s)' % (
      self.pattern_desc,
      getattr(self.function, '__name__', 'anonymous'))

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

