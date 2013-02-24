from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.command import Register
from echomesh.base import CommandFile
from echomesh.base import Merge
from echomesh.util import Log
from echomesh.util import Scope

LOGGER = Log.logger(__name__)

def config(echomesh_instance, *parts):
  if len(parts) < 2:
    return LOGGER.print_error('Usage: config scope command [... command] ')

  try:
    scope = Scope.resolve(parts[1])
  except Exception as e:
    return LOGGER.print_error(e.message)

  if len(parts) == 2:
    try:
      config = open(CommandFile.config_file(scope), 'r').read()
      LOGGER.print('\n' + config)
    except IOError:
      LOGGER.print('(none)')
    return

  try:
    parts = ' '.join(parts[2:])
    configs = Yaml.decode(parts)
  except:
    return LOGGER.print_error("Can't parse yaml argument '%s'" % yaml)

  config = Merge.merge_for_config(*configs)
  if 'default' in scope:
    LOGGER.print_error("Can't make changes to default scope")
  else:
    self._remote(scope=scope, config=config)

CONFIG_HELP = """
The "config" command allows you to set data values in configuration files
on your local node or on every node in your network.

More documentation to come.

"""

SEE_ALSO = ['transfer', 'show scores']

Register.register(config, 'config', CONFIG_HELP)
