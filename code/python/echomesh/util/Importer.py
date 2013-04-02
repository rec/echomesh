from __future__ import absolute_import, division, print_function, unicode_literals

ERROR_MESSAGE = 'You requested a feature that needs the Python library "%s".'
EXCEPTION_TYPE = Exception

class Failure(object):
  def __init__(self, message):
    self.message = message

  def __getattr__(self, key):
    raise EXCEPTION_TYPE(self.message)

def imp(path, name=None, defer_failure=True):
  parts = path.split('.')
  if len(parts) == 1:
    module_path = parts
  elif parts[-2].islower() and not parts[-1].islower():
    module_path = parts[:]
    parts += [parts[-1]]
  else:
    module_path = path[:-1]
  module = '.'.join(module_path)

  try:
    mod = __import__(module)
  except ImportError as e:
    if defer_failure:
      return Failure(ERROR_MESSAGE % (name or module))
    else:
      raise
  else:
    for comp in parts[1:]:
      mod = getattr(mod, comp)
    return mod

