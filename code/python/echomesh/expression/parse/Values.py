from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.expression.parse import Functions
import echomesh.expression.parse.System
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

class ValueException(Exception):
    pass

class ValueRoot(object):
    def _get_function(self, parts, element):
        element = self._get_element(parts, element)
        variable = parts.pop()
        for p in parts:
            element = element.get_child(p)
        try:
            return element.variables[variable]
        except Exception as e:
            self._error('No such', parts + [variable], e)

    def _error(self, message, parts, exception):
        if isinstance(exception, ValueException):
            raise
        exception = (exception and str(exception)) or ''
        raise ValueException('%s %s variable "%s" %s' %
                    (message, self.__class__.__name__.lower(), '.'.join(parts),
                    exception))

    def evaluate(self, parts, evaluator, element):
        try:
            return self._evaluate(parts, evaluator, element)
        except Exception as e:
            self._error("Can't evaluate", parts, e)

    def is_constant(self, parts, element):
        try:
            return self._is_constant(parts, element)
        except Exception as e:
            self._error("Can't evaluate", parts, e)

    def _evaluate(self, parts, evaluator, element):
        return self._get_function(parts, element).evaluate()

    def _is_constant(self, parts, element):
        return self._get_function(parts, element).is_constant()

    def _get_element(self, parts, element):
        return element


class Settings(ValueRoot):
    def _evaluate(self, parts, evaluator, element):
        from echomesh.base import Settings
        return Settings.get(*parts)

    def _is_constant(self, parts, element):
        return False  # TODO: it's inefficient that Settings are non-constant.


class Element(ValueRoot):
    def _get_element(self, parts, element):
        return element.get_root()


class Function(ValueRoot):
    def _evaluate(self, parts, evaluator, element):
        value = evaluator.pop_and_evaluate()
        return Functions.FUNCTIONS.get('.'.join(parts))(value)

    def _is_constant(self, parts, element):
        return True


class Global(ValueRoot):
    def _get_element(self, parts, element):
        from echomesh.element import ScoreMaster
        return ScoreMaster.INSTANCE.get_prefix(parts.pop(0))[1]


class Local(ValueRoot):
    pass


class Parent(ValueRoot):
    def _get_element(self, parts, element):
        return element.parent

class System(ValueRoot):
    def _get_system(self, parts):
        return echomesh.expression.parse.System.get('.'.join(parts))

    def _evaluate(self, parts, evaluator, element):
        return Call.call_recursive(self._get_system(parts).evaluate(element))

    def _is_constant(self, parts, element):
        return self._get_system(parts).is_constant

for c in Settings, Element, Function, Global, Local, Parent, System:
    _REGISTRY.register(c(), c.__name__)
