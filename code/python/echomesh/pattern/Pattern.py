from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Log
from echomesh.util.dict.ReadObservingDictionary import ReadObservingDictionary

LOGGER = Log.logger(__name__)

class Pattern(object):
  # The list of pattern description variables that need to be sent to the
  # evaluator.
  VARIABLES = set()

  def __init__(self, desc):
    desc = ReadObservingDictionary(desc)
    self.patterns = [make_pattern(p) for p in desc.get('pattern', [])]
    self.finish_initialization(desc)
    unread = desc.unread()
    if unread:
      LOGGER.error(
        "For pattern type %s, we didn't use the following parameters: %s" %
        (self.__class__.__name__, ', '.join(unread)))

    self.is_constant = self._is_constant() and (
      all(p.is_constant for p in self.patterns))
    if self.is_constant:
      self._value = self._evaluate();

  def evalulate(self):
    return self._value if self.is_constant else self._evaluate()

  def _evaluate(self):
    return []

  def _is_constant(self):
    return True

  def finish_initialization(self, desc):
    pass
