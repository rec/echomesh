from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Settings
from echomesh.base import Join
from echomesh.command import SetSettings
from echomesh.util import Log

LOGGER = Log.logger(__name__)

def save(_, *values):
  if values:
    SetSettings.set_settings(_, *values)
  files = Settings.save(False)
  if files:
    LOGGER.info('Settings saved to %s.', Join.join_file_names(files))
  else:
    LOGGER.error('There are no settings changes to save.')

HELP = """
  Saves the current settings values.

  Conveniently, you can optionally add values to set before saving.

Examples:
  save
  save speed=50% light.period=40ms
"""
