from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import GetPrefix

from echomesh.expression import Functions
from echomesh.expression import System
from echomesh.expression import Locator

from echomesh.util import Call
from echomesh.util import Log

LOGGER = Log.logger(__name__)

_NAMES = 'configuration', 'element', 'function', 'global', 'local', 'system'

class _Values(object):
  def __init__(self, functions, system):
    self.functions = functions
    self.system = system
    self.table = dict((v, True) for v in _NAMES)

  def evaluate(self, op, evaluator, element=None):
    return self(op, evaluator, element)

  def __call__(self, op, evaluator, element=None):
    return self._interpret(op, evaluator, element, True)

  def is_variable(self, op, element=None):
    return self._interpret(op, None, element, False)

  def _interpret(self, op, evaluator, element, is_evaluating):
    parts = op.split('.')
    if len(parts) == 1:
      cmd = 'function'
    else:
      cmd = parts.pop(0)

    name, function = GetPrefix.get_prefix(self.table, cmd, 'values')
    if name == 'configuration':
      from echomesh.base import Config
      # TODO: Why can't this import be at the top?  Does it even work?!
      return is_evaluating and Config.get(*parts)

    if name == 'function':
      return (is_evaluating and
              self.functions.get('.'.join(parts))(evaluator()))

    if name == 'system':
      func, is_variable = self.system.get('.'.join(parts))
    elif name in ['element', 'global', 'local']:
      func, is_variable = Locator.get_variable(element, name, parts)
    else:
      raise Exception("Shouldn't get here.")

    return Call.call(func) if is_evaluating else is_variable

_VALUES = _Values(Functions.FUNCTIONS, System.SYSTEM)

evaluate = _VALUES.evaluate
is_variable = _VALUES.is_variable

