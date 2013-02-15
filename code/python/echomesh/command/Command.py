from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.command import Config, Registry, Remote, Score, Show
from echomesh.util import Log

LOGGER = Log.logger(__name__)

Registry.register('quit', lambda e: True)

def _fix_exception_message(m, name):
  loc = m.find(')')
  if loc >= 0:
    m = m[loc + 1:]
  m = (m.replace('1', '0').
       replace('2', '1').
       replace('3', '2').
       replace('4', '3'))
  return name + m

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
    LOGGER.print_error(Registry.usage(), exc_info=1)

