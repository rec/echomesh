from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.command import Config, Info, Registry, Remote, Score
from echomesh.util import Log

LOGGER = Log.logger(__name__)

Registry.register('quit', lambda e: True)

def execute(echomesh, line):
  try:
    parts = line.split()
    name = parts.pop(0)
    function = Registry.get(name)
    if not function:
      raise Exception("Didn't understand function %s" % name)
    try:
      return function(echomesh, *parts)
    except TypeError as e:
      raise Exception(_fix_exception_message(str(e), name))

  except Exception as e:
    LOGGER.error(str(e))
    LOGGER.error(Registry.usage())

