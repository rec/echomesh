from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Log
from echomesh.util.dict.ReadObservingDictionary import ReadObservingDictionary
from echomesh.expression import Expression

LOGGER = Log.logger(__name__)

class Pattern(object):
  # The list of pattern description variables that need to be sent to the
  # evaluator.
  VARIABLES = ()
  CONSTANTS = ()
  PATTERN_COUNT = None

  def __init__(self, desc, element):
    desc = ReadObservingDictionary(desc)
    pat = desc.pop('pattern', [])
    if isinstance(pat, dict):
      pat = [pat]
    self.patterns = [make_pattern(p) for p in pat]

    if self.PATTERN_COUNT is not None:
      assert self.PATTERN_COUNT == len(self.patterns), (
        "Pattern type %s expects %s subpatterns but got %d" %
        (self.__class__.__name__, self.PATTERN_COUNT, len(self.patterns)))

    self.dictionary = {}
    self.is_constant = all(p.is_constant for p in self.patterns)
    for k in self.VARIABLES:
      self.dictionary[k] = Expression.expression(dict.get(k), element)
      is_constant = is_constant and self.dictionary[k].is_constant()

    for k in self.CONSTANTS:
      self.dictionary[k] = Expression.constant_expression(dict.get(k))

    unread = desc.unread()
    if unread:
      LOGGER.error(
        "For pattern type %s, we didn't use the following parameters: %s" %
        (self.__class__.__name__, ', '.join(unread)))

    if self.is_constant:
      self._value = self._evaluate();

  def get(self, name):
    return self.dictionary[name].evaluate()

  def evalulate(self):
    return self._value if self.is_constant else self._evaluate()

  def _evaluate(self):
    return []

  def finish_initialization(self, desc):
    pass
