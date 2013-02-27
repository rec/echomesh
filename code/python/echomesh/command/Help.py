from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.command import Register
from echomesh.command import Show

from echomesh.util import Log

LOGGER = Log.logger(__name__)

HELP_TEXT = """
echomesh has the following help topics:

  %s

Type "help TOPIC" for more information - for example, "help quit" or "help run".
"""

def _help(echomesh_instance, *parts):
  if not parts:
    LOGGER.info(HELP_TEXT % Register.join_keys(command_only=False))
  else:
    cmd, parts = parts[0], parts[1:]
    if not parts:
      help_text = Register.get_help(cmd)
      LOGGER.info(help_text or ('No help text available for "%s"' % cmd))
    elif cmd == 'show':
      sub = parts[0]
      help_text = Show.SHOW_REGISTRY.get_help(sub)
      LOGGER.info('\nshow %s:' % sub)
      LOGGER.info(help_text or ('No help text available for "show %s"' % sub))
    else:
      raise Exception("Command '%s' doesn't take any arguments.")


HELP_HELP = """
"help" gives you information about how echomesh commands work.
You can use "?" as a shortcut.

For example, type "help shutdown" or "? quit" to get information about
these commands.

You can also use unambiguous abbreviations like "he shut" or "? q".

For a list of topics, type "help".
For a list of commands, type "help commands".
"""

COMMANDS_HELP = """
Echomesh has the following commands:

  """

Register.register(None, 'commands', COMMANDS_HELP, ['help'])
Register.register(_help, 'help', HELP_HELP)
