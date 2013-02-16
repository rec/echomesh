from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.command import Registry
from echomesh.command import Show

from echomesh.util import Log

LOGGER = Log.logger(__name__)

def _help(echomesh, *parts):
  LOGGER.print()
  if not parts:
    LOGGER.print('echomesh has the following commands: ' + Registry.join_keys())
  else:
    cmd, parts = parts[0], parts[1:]
    if not parts:
      help_text = Registry.get_help(cmd)
      LOGGER.print(help_text or ('No help text available for "%s"' % cmd))
    elif cmd == 'show':
      sub = parts[0]
      help_text = SHOW_REGISTRY.get_help(sub)
      LOGGER.print('show %s:' % sub)
      LOGGER.print(help_text or ('No help text available for "show %s"' % sub))
    else:
      raise Exception("Command '%s' doesn't take any arguments.")


HELP_HELP = """
"help" lets you get information about echomesh commands.

You can get help on the following commands:

  """ + Registry.join_keys()

Registry.register('help', _help, HELP_HELP)
