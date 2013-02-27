from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.command import Broadcast, Config, Register, Remote, Score, Show
from echomesh.command import Transfer

from echomesh.util import FindComment
from echomesh.util import Log
from echomesh.util import Split

LOGGER = Log.logger(__name__)

def _quit(echomesh_instance):
  echomesh_instance.quitting = True
  return True

QUIT_HELP = """
"quit" or q stops all the elements running and quits the echomesh program.
"""


COMMENT_HELP = """
Comment lines start with a # - everything after that is ignored.
"""

Register.register(_quit, 'quit', QUIT_HELP)
Register.register(lambda e: None, '#', COMMENT_HELP)
Register.register(None, 'sample', 'This is a sample with just help')

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

def execute(echomesh_instance, line):
  try:
    line = FindComment.remove_comment(line).strip()
    if not line:
      LOGGER.info('')
      return
    parts = Split.split_words(line)
    name = parts.pop(0)
    function = Register.get(name)
    if not function:
      raise Exception("Didn't understand function %s" % name)
    try:
      return function(echomesh_instance, *parts)
    except TypeError as e:
      LOGGER.error((_fix_exception_message(str(e), name)))

  except Exception as e:
    LOGGER.error("%s\n%s", str(e), usage())

