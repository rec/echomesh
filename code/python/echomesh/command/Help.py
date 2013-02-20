from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.command import Register
from echomesh.command import Show

from echomesh.util import Log

LOGGER = Log.logger(__name__)

HELP_TEXT = """
echomesh knows the following commands:

  %s

and also accepts abbreviations like q, br or shut.
"""

def _help(echomesh, *parts):
  if not parts:
    LOGGER.print(HELP_TEXT % Register.join_keys())
  else:
    cmd, parts = parts[0], parts[1:]
    if not parts:
      help_text = Register.get_help(cmd)
      LOGGER.print(help_text or ('No help text available for "%s"' % cmd))
    elif cmd == 'show':
      sub = parts[0]
      help_text = Show.SHOW_REGISTRY.get_help(sub)
      LOGGER.print('\nshow %s:' % sub)
      LOGGER.print(help_text or ('No help text available for "show %s"' % sub))
    else:
      raise Exception("Command '%s' doesn't take any arguments.")


HELP_HELP = """
"help" gives you information about how echomesh commands work - "he" or "?"
also work.

You can get help on the following commands:

  %s

for example, "help shutdown" or "help quit"
and you can also use abbreviations like "? shut" or "? q"

""" + Register.join_keys()

Register.register('help', _help, HELP_HELP)