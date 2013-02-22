from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.command import Broadcast, Config, Register, Remote, Score, Show
from echomesh.command import Transfer

from echomesh.util import Log
from echomesh.util import FindComment

LOGGER = Log.logger(__name__)

def _quit(echomesh):
  echomesh.quitting = True
  return True

QUIT_HELP = """
"quit" or q stops all the elements running and quits the echomesh program.
"""


COMMENT_HELP = """
Comment lines start with a # - everything after that is ignored.
"""

Register.register('quit', _quit, QUIT_HELP)
Register.register('#', lambda e: None, COMMENT_HELP)
Register.register('sample', None, 'This is a sample with just help')

# Must be the last one to load.
from echomesh.command import Help

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
  return 'Valid commands are: ' + Register.join_keys()

def execute(echomesh, line):
  try:
    line = FindComment.remove_comment(line).strip()
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

