from __future__ import absolute_import, division, print_function, unicode_literals

import copy

import echomesh.base.Config

from echomesh.base import Args
from echomesh.base import CommandFile
from echomesh.base import Join
from echomesh.base import Merge
from echomesh.base import MergeConfig
from echomesh.base import Yaml
from echomesh.command import Register
from echomesh.util import Context
from echomesh.util import Log

LOGGER = Log.logger(__name__)

def register():
  Register.register_all(
    get=(get, GET_HELP),
    save=(save, SAVE_HELP),
    set=(_set, SET_HELP),
  )

def get(_, value, *more):
  errors = []
  successes = []
  for v in (value,) + more:
    try:
      successes.append([v, echomesh.base.Config.get(*v.split('.'))])
    except:
      errors.append(v)

  for value, result in successes:
    LOGGER.info('%s=%s', value, result)
  if errors:
    LOGGER.error('Didn\'t understand %s', Join.join_words(errors))

def save(_, *values):
  if values:
    _set(_, *values)
  if MergeConfig.LOCAL_CHANGES:
    config_file, data = _get_raw_file()
    data.append(Yaml.encode_one(MergeConfig.LOCAL_CHANGES))
    MergeConfig.LOCAL_CHANGES = {}
    _raw_write(config_file, data)
    LOGGER.info('Saved to file %s.', config_file)
  else:
    LOGGER.error('There are no changes to save.')

def _set(_, *values):
  if values:
    assignments = Args.split_args(values)
    MergeConfig.merge_assignments(echomesh.base.Config.CONFIG, assignments)

    for address, value in assignments:
      LOGGER.info('Set %s=%s', '.'.join(address), value)
    if assignments:
      echomesh.base.Config.update_clients()
  elif MergeConfig.LOCAL_CHANGES:
    LOGGER.info(Yaml.encode_one(MergeConfig.LOCAL_CHANGES))
  else:
    LOGGER.info('You have made no changes.')

def _get_file(context='master'):
  config_file = CommandFile.config_file(context)
  return config_file, Yaml.read(config_file)

def _clean(_):
  config_file, results = _get_file()
  if results and len(results) > 1:
    Yaml.write(config_file, Merge.merge(*results))

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
  # Bug: we'll never be able to override command line arguments this way.  :-D
  echomesh.base.Config.recalculate()

SET_HELP = """
  Sets one or more configuration variables.  These changes are only present in
  memory and will be lost when the program ends - you need to use config save
  to make them permanent.

Examples:
  set speed=50%
  set speed=10% light.period=40ms
"""

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

GET_HELP = """
  Prints one or more configuration variables.

Examples:
  config.get speed
  config.get audio.input.enabled audio.output.enabled
"""

register()
