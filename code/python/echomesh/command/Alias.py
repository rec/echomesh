from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Log
from echomesh.command import Aliases
from echomesh.command import Show

LOGGER = Log.logger(__name__)

def alias(instance, *path):
  aliases = Aliases.instance()
  if not path:
    Show.aliases()
    return
  alias = path[0]
  result = aliases.get_prefix(alias)

  if len(path) == 1:
    if result:
      LOGGER.info('Alias %s=%s', result[0], result[1])
    else:
      LOGGER.error('Don\'t understand alias %s.' % alias)
    return

  parts = (p.strip() for p in ' '.join(path[1:]).split('&'))
  parts = [p for p in parts if p]
  if not parts:
    LOGGER.error('Don\'t understand alias %s.', ' '.join(path))
    return

  if 'delete'.startswith(parts[0]):
    if len(parts) > 1:
      LOGGER.error('alias delete takes no arguments: %s.', ' '.join(path))

    elif not result:
      LOGGER.error('Don\'t understand alias %s.' % alias)
    else:
      del aliases[result[0]]
      LOGGER.info('Alias %s deleted.', result[0])
  else:
    aliases[alias] = parts
    LOGGER.info('Alias %s=%s', alias, parts)

HELP = """
  The alias command allows you to attach one or more commands to a
  shorthand alias.

alias:
  Lists all the commands - just like show alias

alias <name>:
  Lists the alias attached to just that one command, if any

alias <name> delete:
  Deletes the alias attached to that command, if any.

alias <name> <command> [& <command> & <command>]:
  Attaches one or more commands to that alias name.

"""
