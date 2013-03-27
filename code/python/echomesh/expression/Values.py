from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Config
from echomesh.base import GetPrefix
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class Values(object):
  def __init__(self, elements):
    self.functions = {}
    self.elements = elements
    not_variable = lambda x: False
    self.table = dict((v, getattr(self, v)) for v in VALUES)
    self.system = {}

  def evaluate(self, op, evaluator):
    return self._interpret(op, evaluator, True)

  def is_variable(self, op):
    return self._interpret(op, None, False)

  def _interpret(self, op, evaluator, is_evaluating):
    parts = op.split('.')
    if len(parts) == 1:
      cmd = 'function'
    else:
      cmd = parts.pop(0)

    name, function = GetPrefix.get_prefix(self.table, cmd, 'values')
    if name == 'configuration':
      return is_evaluating and Config.get(*parts)

    if name == 'function':
      return is_evaluating and self.functions['.'.join(parts)](evaluator())

    if name == 'system':
      func, is_variable = self.system['.'.join(parts)]
    elif name in ['element', 'global', 'local']:
      func, is_variable = self.elements(name, parts)
    else:
      raise Exception("Shouldn't get here.")

    if is_evaluating:
      while callable(func):
        func = func()
      return func
    else:
      return is_variable

