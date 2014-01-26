from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Log
from echomesh.util.dict.ReadObservingDictionary import ReadObservingDictionary
from echomesh.expression import Expression
from echomesh.pattern import PatternDesc

LOGGER = Log.logger(__name__)

USE_PATTERN = False

class Pattern(object):
  CONSTANTS = ()
  VARIABLES = ()

  OPTIONAL_CONSTANTS = ()
  OPTIONAL_VARIABLES = ()
  PATTERN_COUNT = None

  def __init__(self, desc, element, name):
    self.name = name
    self.element_name = element.class_name()
    desc = ReadObservingDictionary(desc)
    pat = desc.pop('pattern', [])
    if isinstance(pat, dict):
      pat = [pat]
    # TODO: we need to be able to reference subpatterns
    self._patterns = [PatternDesc.make_pattern(element, 'NONAME', p) for p in pat]

    if self.PATTERN_COUNT is not None:
      assert self.PATTERN_COUNT == len(self._patterns), (
        "Pattern type %s expects %s subpatterns but got %d" %
        (self.__class__.__name__, self.PATTERN_COUNT, len(self._patterns)))

    self.dictionary = {}
    is_constant = all(p.is_constant for p in self._patterns)
    missing = []
    for k in self.VARIABLES:
      v = desc.get(k)
      if v is None:
        missing.append(k)
      else:
        self.dictionary[k] = Expression.expression(v, element)
        is_constant = is_constant and self.dictionary[k].is_constant()

    for k in self.OPTIONAL_VARIABLES:
      self.dictionary[k] = Expression.expression(desc.get(k), element)
      is_constant = is_constant and self.dictionary[k].is_constant()

    for k in self.CONSTANTS:
      v = desc.get(k)
      if v is None:
        missing.append(k)
      else:
        self.dictionary[k] = Expression.constant_expression(v)

    for k in self.OPTIONAL_CONSTANTS:
      self.dictionary[k] = Expression.constant_expression(desc.get(k))

    if missing:
      raise Exception('%s is missing required arguments %s' %
                      (self, ', '.join(missing)))

    unread = desc.unread()
    if unread:
      LOGGER.error(
        "For pattern type %s, we didn't use the following parameters: %s",
        self.__class__.__name__, ', '.join(unread))

    self.is_constant = is_constant
    if self.is_constant:
      self._value = self._evaluate();

  def get(self, name):
    return self.dictionary[name].evaluate()

  def patterns(self):
    return [p.evaluate() for p in self._patterns]

  def evaluate(self):
    return self._value if self.is_constant else self._evaluate()

  def _evaluate(self):
    return []

  def __str__(self):
    return 'pattern "%s" in element "%s"' % (self.name, self.element_name)

