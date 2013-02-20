from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.command import Config, Help, Register, Remote, Score, Show
from echomesh.util import Log

LOGGER = Log.logger(__name__)

Register.register('quit', lambda e: True,
                  'Quits the echomesh program.')

def _fix_exception_message(m, name):
  loc = m.find(')')
  if loc >= 0:
    m = m[loc + 1:]
  m = (m.replace('1', '0').
       replace('2', '1').
       replace('3', '2').
       replace('4', '3').
       replace('1 arguments', '1 argument'))
  return name + m

def usage():
  return 'Valid options are:' + Register.join_keys()

def execute(echomesh, line):
  try:
    line = line.strip()
    if not line:
      LOGGER.print('')
      return
    parts = line.split()
    name = parts.pop(0)
    function = Register.get(name)
    if not function:
      raise Exception("Didn't understand function %s" % name)
    try:
      return function(echomesh, *parts)
    except TypeError as e:
      LOGGER.print_error((_fix_exception_message(str(e), name)), exc_info=0)

  except Exception as e:
    LOGGER.print_error("%s\n%s", str(e), usage())
