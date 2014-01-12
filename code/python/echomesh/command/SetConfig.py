from __future__ import absolute_import, division, print_function, unicode_literals

import six

from echomesh.base import Config
from echomesh.base import Leafs
from echomesh.base import Yaml
from echomesh.command import REGISTRY
from echomesh.util import Log

LOGGER = Log.logger(__name__)

def set_config(_, *values):
  if values:
    assignment = Leafs.leafs(Config.assign(values))
    for address, value in six.iteritems(assignment):
      LOGGER.info('Set %s=%s', '.'.join(address), value)
    Config.update_clients()
  elif Config.MERGE_CONFIG.has_changes():
    LOGGER.info(Yaml.encode_one(dict(Config.MERGE_CONFIG.get_changes())))
  else:
    LOGGER.info('You have made no changes.')

SET_HELP = """
  Sets one or more configuration variables.  These changes are only present in
  memory and will be lost when the program ends - you need to use config save
  to make them permanent.

Examples:
  set speed=50%
  set speed=10% light.period=40ms
"""

REGISTRY.register(set_config, 'set', SET_HELP)
