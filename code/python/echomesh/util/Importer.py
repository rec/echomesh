from __future__ import absolute_import, division, print_function, unicode_literals

ERROR_MESSAGE = 'You requested a feature that needs the Python library "%s".'
EXCEPTION_TYPE = Exception

class _ImportFailure(object):
  def __init__(self, name):
    self.name = name

  def __getattr__(self, key):
    raise EXCEPTION_TYPE(ERROR_MESSAGE % self.name)

def imp(module):
  try:
    return __import__(module)
  except ImportError:
    return _ImportFailure(module)
