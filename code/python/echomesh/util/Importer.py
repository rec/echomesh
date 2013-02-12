from __future__ import absolute_import, division, print_function, unicode_literals

ERROR_MESSAGE = 'You requested a feature that needs the Python library "%s".'
EXCEPTION_TYPE = Exception

class Failure(object):
  def __init__(self, message):
    self.message = message

  def __getattr__(self, key):
    raise EXCEPTION_TYPE(self.message)

def imp(module, name=None):
  try:
    return __import__(module)
  except ImportError:
    return Failure(ERROR_MESSAGE % (name or module))
