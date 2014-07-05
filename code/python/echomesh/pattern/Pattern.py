from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import re
import six

from echomesh.expression import ConstantExpression
from echomesh.expression import Expression
from echomesh.pattern.Registry import make_pattern
from echomesh.util import Log
from echomesh.util.dict.ReadObservingDictionary import ReadObservingDictionary
from echomesh.util.string.Split import split_on_commas

LOGGER = Log.logger(__name__)

class PatternException(Exception):
  pass

class Pattern(object):
  SETTINGS = {}
  HELP = ''
  PATTERN_COUNT = None

  def __init__(self, desc, element, name):
    self.name = name
    self.element = element
    desc = ReadObservingDictionary(desc)
    pat = desc.pop('pattern', [])
    if isinstance(pat, dict):
      pat = [pat]
    elif isinstance(pat, six.string_types):
      pat = split_on_commas(pat)
    self._patterns = [make_pattern(element, p) for p in pat]

    if self.PATTERN_COUNT is not None:
      assert self.PATTERN_COUNT == len(self._patterns), (
        "Pattern type %s expects %s subpatterns but got %d" %
        (self.__class__.__name__, self.PATTERN_COUNT, len(self._patterns)))

    self.dictionary = {}
    self.is_constant = all(p.is_constant for p in self._patterns)

    missing = []
    self.constants = set()
    for k, v in self.SETTINGS.items():
      const = v.get('constant') or False
      if const:
        self.constants.add(k)
      value = desc.get(k, v.get('default'))
      if value is None and 'default' not in v:
        missing.append(k)
      else:
        if const:
          expression = ConstantExpression.constant_expression(value)
        else:
          expression = Expression.expression(value, element)
        self.dictionary[k] = expression
        self.is_constant = self.is_constant and expression.is_constant()

    if missing:
      raise Exception('%s is missing required arguments %s' %
                      (self, ', '.join(missing)))

    unread = desc.unread()
    if unread:
      LOGGER.error(
        "For pattern type %s, we didn't use the following parameters: %s",
        self.__class__.__name__, ', '.join(unread))

    self._in_precompute = True
    self._precompute()
    self._in_precompute = False
    if self.is_constant:
      self._value = self._evaluate();

  def get(self, name):
    if self._in_precompute and name not in self.constants:
      raise PatternException(
          'Tried to use non-constant value %s in initialization' % name)
    return self.dictionary[name].evaluate()

  def get_raw(self, name):
    try:
      return self.get(name)
    except PatternException:
      raise
    except:
      return getattr(self.dictionary[name], 'original_expression')

  def get_dict(self, *names):
    return dict((name, self.get(name)) for name in names)

  def patterns(self):
    return [p.evaluate() for p in self._patterns]

  def evaluate(self):
    return self._value if self.is_constant else self._evaluate()

  def _evaluate(self):
    return []

  def _precompute(self):
    pass

  def __str__(self):
    return 'pattern "%s" in element "%s"' % (
      self.name, self.element.class_name())


def copy_settings(cl, **kwds):
  return dict(copy.deepcopy(cl.SETTINGS), **kwds)

def copy_const_settings(cl, **kwds):
  parent = copy.deepcopy(cl.SETTINGS)
  for k, v in parent.items():
    v['constant'] = True

  return dict(parent, **kwds)
