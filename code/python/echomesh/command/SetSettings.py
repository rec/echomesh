from __future__ import absolute_import, division, print_function, unicode_literals

import six

from echomesh.base import Settings
from echomesh.base import Leafs
from echomesh.base import Yaml
from echomesh.command import Registry
from echomesh.util import Log

LOGGER = Log.logger(__name__)

def set_settings(_, *values):
    if values:
        assignment = Leafs.leafs(Settings.assign(values))
        for address, value in six.iteritems(assignment):
            LOGGER.info('Set %s=%s', '.'.join(address), value)
        Settings.update_clients()
    elif Settings.MERGE_SETTINGS.has_changes():
        LOGGER.info(
            Yaml.encode_one(dict(Settings.MERGE_SETTINGS.get_changes())))
    else:
        LOGGER.info('You have made no changes.')

SET_HELP = """
  Sets one or more settings variables.  These changes are only present in
  memory and will be lost when the program ends - you need to use settings save
  to make them permanent.

Examples:
  set speed=50%
  set speed=10% light.period=40ms
"""

Registry.registry().register(set_settings, 'set', SET_HELP)
