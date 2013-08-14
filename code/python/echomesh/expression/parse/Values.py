from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.expression.parse import Functions
from echomesh.expression.parse import System
from echomesh.util import Call
from echomesh.util.registry.Registry import Registry

_REGISTRY = Registry('expression values')

def _get_value_function(value):
   parts = value.split('.')
   if len(parts) == 1:
     cmd = 'function'
   else:
     cmd = parts.pop(0)
   return _REGISTRY.function(cmd), parts

def is_constant(value, element):
  value_class, parts = _get_value_function(value)
  return value_class.is_constant(parts, element)

def evaluate(value, evaluator, element):
  value_class, parts = _get_value_function(value)
  return value_class.evaluate(parts, evaluator, element)

class ValueRoot(object):
  def _get_function(self, parts, element):
    element = self._get_element(parts, element)
    variable = parts.pop()
    for p in parts:
      element = element.get_child(p)
    return element.variables[variable]

  def evaluate(self, parts, evaluator, element):
    return Call.call(self._get_function(parts, element))

  def is_constant(self, parts, element):
    return self._get_function(parts, element).is_constant()

  def _get_element(self, parts, element):
    pass

class Configuration(ValueRoot):
  def evaluate(self, parts, evaluator, element):
    from echomesh.base import Config
    return Config.get(*parts)

  def is_constant(self, parts, element):
    return False  # TODO: it's inefficient that Configs are non-constant.

class Element(ValueRoot):
  def _get_element(self, parts, element):
    return element.get_root()

class Function(ValueRoot):
  def evaluate(self, parts, evaluator, element):
    value = evaluator.pop_and_evaluate()
    return Functions.FUNCTIONS.get('.'.join(parts))(value)

  def is_constant(self, parts, element):
    return True

class Global(ValueRoot):
  def _get_element(self, parts, element):
    from echomesh.element import ScoreMaster
    return ScoreMaster.INSTANCE.get_prefix(parts.pop(0))[1]

class Local(ValueRoot):
  def _get_element(self, parts, element):
    return element

class Parent(ValueRoot):
  def _get_element(self, parts, element):
    return element.parent

class System(ValueRoot):
  def _get_system(self, parts):
    return System.get('.'.join(parts))

  def is_constant(self, parts):
    return self._get_system(parts).is_constant

  def evaluate(self, parts):
    return Call.call(self._get_system(parts).function)

_REGISTRY.register(Configuration(), 'configuration')
_REGISTRY.register(Element(), 'element')
_REGISTRY.register(Function(), 'function')
_REGISTRY.register(Global(), 'global')
_REGISTRY.register(Local(), 'local')
_REGISTRY.register(Parent(), 'parent')
_REGISTRY.register(System(), 'system')
