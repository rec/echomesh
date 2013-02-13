from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.command import Registry
from echomesh.base import CommandFile
from echomesh.base import Merge
from echomesh.util import Log
from echomesh.util import Scope

LOGGER = Log.logger(__name__)

def config(echomesh, *parts):
  if len(parts) < 2:
    return LOGGER.error('Usage: config scope command [... command] ')

  try:
    scope = Scope.resolve(parts[1])
  except Exception as e:
    return LOGGER.error(e.message)

  if len(parts) == 2:
    try:
      config = open(CommandFile.config_file(scope), 'r').read()
      LOGGER.info('\n' + config)
    except IOError:
      LOGGER.info('(none)')
    return

  try:
    parts = ' '.join(parts[2:])
    configs = Yaml.decode(parts)
  except:
    return LOGGER.error("Can't parse yaml argument '%s'" % yaml)

  config = Merge.merge_strict(*configs)
  if '0.local' in scope:
    echomesh.socket.router({'type': 'config', 'config': config,
                                  'scope': scope})
  elif '4.default' in scope:
    LOGGER.error("Can't make changes to default scope")
  else:
    self._remote(scope=scope, config=config)

Registry.register_all(config=config)
