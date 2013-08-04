from __future__ import absolute_import, division, print_function, unicode_literals

import copy

from echomesh.base import CommandFile
from echomesh.base import Config
from echomesh.base import Join
from echomesh.base import Merge
from echomesh.base import MergeConfig
from echomesh.base import Yaml
from echomesh.command import CommandRegistry
from echomesh.command import SetConfig
from echomesh.util import Log
from echomesh.util import Quit

LOGGER = Log.logger(__name__)

def _file_name(file_names):
  if len(file_names) == 1:
    return 'file %s' % file_names[0]
  else:
    return 'files %s' % Join.join_words(file_names)

# Automatically save any changed variables on exit.
def _save_atexit():
  files = Config.get('autosave') and Config.MERGE_CONFIG.save()
  if files:
    LOGGER.info('Configuration automatically saved to %s.', _file_name(files))

Quit.register_atexit(_save_atexit)

def _save(_, *values):
  if values:
    SetConfig.set_config(_, *values)
  files = Config.MERGE_CONFIG.save()
  if files:
    LOGGER.info('Configuration saved to %s.', _file_name(files))
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


