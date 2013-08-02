from __future__ import absolute_import, division, print_function, unicode_literals

import copy

from echomesh.base import CommandFile
from echomesh.base import Config
from echomesh.base import Merge
from echomesh.base import MergeConfig
from echomesh.base import Yaml
from echomesh.command import CommandRegistry
from echomesh.command import SetConfig
from echomesh.util import Log
from echomesh.util import Quit

LOGGER = Log.logger(__name__)

# Automatically save any changed variables on exit.
def _save_atexit():
  config_file = Config.get('autosave') and _raw_save()
  if config_file:
    LOGGER.info('Configuration automatically saved to file %s.', config_file)

Quit.register_atexit(_save_atexit)

def _save(_, *values):
  if values:
    SetConfig.set_config(_, *values)
  config_file = _raw_save()
  if config_file:
    LOGGER.info('Configuration saved to file %s.', config_file)
  else:
    LOGGER.error('There are no configuration changes to save.')

SAVE_HELP = """
  Saves the current configuration values.

  Conveniently, you can optionally add values to set before saving.

Examples:
  save
  save speed=50% light.period=40ms
"""

CommandRegistry.register(_save, 'save', SAVE_HELP)

def _raw_save(context='master'):
  if MergeConfig.LOCAL_CHANGES:
    config_file = CommandFile.config_file(context)
    with open(config_file) as f:
      data = [d for d in f.read().split(Yaml.SEPARATOR) if d.strip()]
    if len(data) < 2:
      data.append(Yaml.encode_one(MergeConfig.LOCAL_CHANGES))
    else:
      old_data = Yaml.decode_one(data[1])
      old_data = Merge.merge(old_data, MergeConfig.LOCAL_CHANGES)
      data[1] = Yaml.encode_one(old_data)
    MergeConfig.LOCAL_CHANGES = {}
    _raw_write(config_file, data)
    return config_file

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

