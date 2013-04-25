from __future__ import absolute_import, division, print_function, unicode_literals

import copy

from echomesh.base import CommandFile
from echomesh.base import Config
from echomesh.base import Merge
from echomesh.base import MergeConfig
from echomesh.base import Yaml
from echomesh.command import Register
from echomesh.command import SetConfig
from echomesh.util import Log

LOGGER = Log.logger(__name__)

def save_config(_, *values):
  if values:
    SetConfig.set_config(_, *values)
  if MergeConfig.LOCAL_CHANGES:
    config_file, data = _get_raw_file()
    data = [d for d in data if d.strip()]
    if len(data) < 2:
      data.append(Yaml.encode_one(MergeConfig.LOCAL_CHANGES))
    else:
      old_data = Yaml.decode_one(data[1])
      Merge.merge(old_data, MergeConfig.LOCAL_CHANGES)
      data[1] = Yaml.encode_one(old_data)
    MergeConfig.LOCAL_CHANGES = {}
    _raw_write(config_file, data)
    LOGGER.info('Saved to file %s.', config_file)
  else:
    LOGGER.error('There are no changes to save.')

def _get_raw_file(context='master'):
  config_file = CommandFile.config_file(context)
  with open(config_file) as f:
    data = f.read()
  return config_file, filter(None, data.split(Yaml.SEPARATOR))

def _raw_write(config_file, data):
  first = True
  # TODO: open a temp file and write at the end.
  with open(config_file, 'wb') as f:
    for d in data:
      if d:
        if first:
          first = False
        else:
          f.write(Yaml.SEPARATOR)
        f.write(d)
  Config.recalculate()

CHANGES_HELP = """
  Shows what configuration values have been changed since the last save.

"""

SAVE_HELP = """
  Saves the current configuration values.

  Conveniently, you can optionally add values to set before saving.

Examples:
  save
  save speed=50% light.period=40ms
"""

Register.register(save_config, 'save', SAVE_HELP)
