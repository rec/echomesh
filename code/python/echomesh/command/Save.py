from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Config
from echomesh.base import Join
from echomesh.command import SetConfig
from echomesh.util import Log

LOGGER = Log.logger(__name__)

def save(_, *values):
  if values:
    SetConfig.set_config(_, *values)
  files = Config.save(False)
  if files:
    LOGGER.info('Configuration saved to %s.', Join.join_file_names(files))
  else:
    LOGGER.error('There are no configuration changes to save.')

HELP = """
  Saves the current configuration values.

  Conveniently, you can optionally add values to set before saving.

Examples:
  save
  save speed=50% light.period=40ms
"""
