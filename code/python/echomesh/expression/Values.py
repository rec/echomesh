from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import GetPrefix
from echomesh.base import Enum
from echomesh.expression import Functions
from echomesh.expression import System
from echomesh.expression import Locator
from echomesh.util import Call

Names = Enum.Enum('CONFIGURATION', 'ELEMENT', 'FUNCTION', 'GLOBAL', 'LOCAL',
                  'PARENT', 'SYSTEM')

ELEMENT_NAMES = set([Names.ELEMENT, Names.GLOBAL, Names.LOCAL, Names.PARENT])

class _Values(object):
  def __init__(self, functions, system):
    self.functions = functions
    self.system = system
    self.table = dict((name.lower(), True) for name in Names)

  def evaluate(self, op, evaluator, element):
    return self._interpret(op, evaluator, element, True)

  def is_constant(self, op, element):
    return self._interpret(op, None, element, False)

  def _interpret(self, op, evaluator, element, is_evaluating):
    parts = op.split('.')
    if len(parts) == 1:
      cmd = 'function'
    else:
      cmd = parts.pop(0)

    name, _ = GetPrefix.get_prefix(self.table, cmd)
    name = getattr(Names, name.upper())
    if name == Names.CONFIGURATION:
      from echomesh.base import Config
      # TODO: Why can't this import be at the top?  Does it even work?!
      return is_evaluating and Config.get(*parts)

    if name == Names.FUNCTION:
      return (is_evaluating and
              self.functions.get('.'.join(parts))(evaluator.evaluate()))

    if name == Names.SYSTEM:
      func, is_constant = self.system.get('.'.join(parts))
      if not is_evaluating:
        return is_constant
    elif name in ELEMENT_NAMES:
      func = Locator.get_variable(element, Names.reverse(name).lower(), parts)
    else:
      raise Exception("Shouldn't get here.")

    return Call.call(func) if is_evaluating else func.is_constant()

_VALUES = _Values(Functions.FUNCTIONS, System.SYSTEM)

evaluate = _VALUES.evaluate
is_constant = _VALUES.is_constant
