from __future__ import absolute_import, division, print_function, unicode_literals

def constant(value, _):
  return value

def variable(value, _):
  return value()

def function(value, evaluator):
  return value(evaluator.evaluate())

class Variables(object):
  def __init__(self, **constants):
    self.variables = {}

  def evaluate(self, name, evaluator):
    return self.variables[name](evaluator)

  def add(self, method, name, value):
    assert name not in self.variables
    self.variables[name] = method
