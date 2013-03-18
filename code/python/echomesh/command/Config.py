from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.command import Register
from echomesh.base import CommandFile
from echomesh.base import Merge
from echomesh.base import Yaml
from echomesh.util import Log
from echomesh.util import Scope

LOGGER = Log.logger(__name__)

# TODO: this doesn't work!
def config(_, *parts):
  if len(parts) < 2:
    return LOGGER.error('Usage: config scope command [... command] ')

  try:
    scope = Scope.resolve(parts[1])
  except Exception as e:
    return LOGGER.error(e.message)

  if len(parts) == 2:
    try:
      cfg = open(CommandFile.config_file(scope), 'r').read()
      LOGGER.info('\n' + cfg)
    except IOError:
      LOGGER.info('(none)')
    return

  parts = ' '.join(parts[2:])
  try:
    configs = Yaml.decode(parts)
  except:
    return LOGGER.error("Can't parse yaml argument '%s'", parts)

  cfg = Merge.merge_for_config(*configs)
  if 'default' in scope:
    LOGGER.error("Can't make changes to default scope")
  else:
    # self._remote(scope=scope, config=cfg)
    pass

CONFIG_HELP = """
The "config" command allows you to set data values in configuration files
on your local node or on every node in your network.

More documentation to come.

"""

SEE_ALSO = ['transfer', 'show scores']

Register.register(config, 'config', CONFIG_HELP)
