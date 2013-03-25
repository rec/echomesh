from __future__ import absolute_import, division, print_function, unicode_literals

# pylint: disable=W0611
from echomesh.command import Broadcast, Context, Register, Remote, Score, Show
from echomesh.command import Transfer

# Must be the last one to load.
from echomesh.command import Help

# pylint: enable=W0611

from echomesh.util import FindComment
from echomesh.util import Log
from echomesh.util import Split

LOGGER = Log.logger(__name__)

COMMENT_HELP = """
Comment lines start with a # - everything after that is ignored.
"""

Register.register(lambda e: None, '#', COMMENT_HELP)
Register.register(None, 'sample', 'This is a sample with just help')

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
      e.message = _fix_exception_message(e.message, name)
      LOGGER.error()

  except Exception as e:
    LOGGER.error("\n%s", usage())

