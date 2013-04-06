from __future__ import absolute_import, division, print_function, unicode_literals

import copy

import echomesh.base.Config

from echomesh.base.Config import CONFIG
from echomesh.base import CommandFile
from echomesh.base import Join
from echomesh.base import Merge
from echomesh.base import MergeConfig
from echomesh.base import Yaml
from echomesh.command import Register
from echomesh.util import Context
from echomesh.util import Log

LOGGER = Log.logger(__name__)


Register.register_all(
  changes=(_changes, CHANGES_HELP),
  clean=(_clean, CLEAN_HELP),
  get=(_get, GET_HELP),
  save=(_save, SAVE_HELP),
  set=(_set, SET_HELP),
)

def _get_file(context='master'):
  config_file = CommandFile.config_file(context)
  return config_file, Yaml.read(config_file)

def _clean(_):
  config_file, results = _get_file()
  if results and len(results) > 1:
    Yaml.write(config_file, Merge.merge(*results))

def _get(_, value, *more):
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
    LOGGER.error('Didn\'t understand %s',
                 Join.join_words(errors))

_LOCAL_CHANGES = {}

def _get_raw_file(context='master'):
  config_file = CommandFile.config_file(context)
  with open(config_file) as f:
    data = f.read()
  return config_file, data.split(Yaml.SEPARATOR)

def _raw_write(config_file, data):
  first = True
  # TODO: open a temp file and write at the end.
  with open(config_file, 'wb') as f:
    for d in data:
      if first:
        first = False
      else:
        f.write(Yaml.SEPARATOR)
      f.write(data[d])
  # Bug: we'll never be able to override command line arguments this way.  :-D
  echomesh.base.Config.recalculate()

def _set(_, value, *more):
  values = (value, ) + more
  for address, value in MergeConfig.merge_assignments(CONFIG, values):
    LOGGER.info('Set %s=%s', '.'.join(address), value)
    cfg = _LOCAL_CHANGES
    for a in address[:-1]:
      cfg = cfg.setdefault(a, {})
    cfg[address[-1]] = value

def _save(values, contexts):
  global _LOCAL_CHANGES
  if _LOCAL_CHANGES:
    config_file, data = _get_raw_file()
    data.append(_LOCAL_CHANGES)
    _LOCAL_CHANGES = {}
    _raw_write(config_file, data)
    LOGGER.info('Saved to file %s.', config_file)
  else:
    LOGGER.error('There are no changes to save.')

def _changes(values, contexts):
  LOGGER.info(Yaml.encode_one(_LOCAL_CHANGES))



CONFIG_HELP = """
The "config" commands allows you to manipulate configuration values in files
on your local node or any every node in your network.

"config get":
  Prints one or more configuration variables.

Examples:
  config.get speed
  config.get audio.input.enabled audio.output.enabled


"config set":
  Sets one or more configuration variables.  These changes are only present in
  memory and will be lost when the program ends - you need to use config save
  to make them permanent.

Examples:
  config set speed=50%
  config set speed=10% light.period=40ms


"config changes"
  Shows what configuration values have been changed since the last save.


"config save":
  Saves the current configuration values.

  Conveniently, you can optionally add values to set before saving.

Examples:
  config save
  config save speed=50% light.period=40ms


"config undo"
  Undoes the save operation.  If you haven't saved yet, the first call to undo
  will reset to the previous save;  then subsequent calls will undo each
  previous save, back to an empty file.

  Two special forms exist:
  "undo all" clears to an empty document.
  "undo top" undoes to the "original document" - the very first
  version of the document.


"config redo":
  Reverses the effects of "config undo".


"config clean":
  Because each change is saved separately in your configuration file, the
  files can become long and redundant.  Cleaning them removes this redundancy,
  but you lose all your comments and your ability to undo.


Setting The Context.

An optional "context" argument says which machines are affected.
This works for all commands except "config get".

Valid contexts are:
  master:  all machines
  local:  the current machine.
  platform:  all machines with the same platform.
  tag/<tagname>: all machines with a given tag.
  name/<echomesh name>:  any machine with a given echomesh name

You can have multiple context arguments and they can appear anywhere.

Examples:

  # Just set the brightness for this machine.
  config set local light.brightness=50%

  # Same.
  config local set light.brightness=50%

  # Set the brightness everywhere.
  config global set light.brightness=50%

"""

SEE_ALSO = ['show context']

Register.registe(config, 'config', CONFIG_HELP, SEE_ALSO)



def config(_, *parts):
  if len(parts) < 1:
    return LOGGER.error(USAGE)

  contexts = []
  command = ''
  values = []
  for p in parts:
    try:
      contexts.append(Context.resolve(p))
    except:
      if command:
        values.append(p)
      else:
        command = p

  if not command:
    return LOGGER.error(USAGE)

  try:
    key, cmd = _REGISTRY.get_key_and_value(command)
  except:
    return LOGGER.error('Didn\'t understand command "config %s"', command)

  if values:
    if key in NEEDS_NO_VALUES:
      return LOGGER.error('"config %s" doesn\'t take any values.', key)
  else:
    if key in NEEDS_VALUES:
      return LOGGER.error('"config %s" needs to be given values.', key)

  return cmd(values, contexts)

_REGISTRY = Registry('Config commands')

NEEDS_NO_VALUES = set(('clean', 'changes', 'save'))
NEEDS_VALUES = set(('set', 'get'))

from echomesh.util.Registry import Registry

def _redo(values, contexts):
  if not _REDO_STACK:
    return LOGGER.error('There\'s nothing to redo.')
  if len(values) > 1:
    return LOGGER.error('"config undo" takes at most one argument.')
  if values:
    if values[0] == 'all':
      is_all = True
    else:
      return LOGGER.error('"config redo" doesn\'t understand %s.', values[0])
  else:
    is_all = False

  config_file, data = _get_raw_file()

  while _REDO_STACK:
    is_local, value = _REDO_STACK.pop()
    if is_local:
      global _LOCAL_CHANGES
      _LOCAL_CHANGES = value
      LOGGER.info('Redid local changes.')
    else:
      data.append(value)
    if not is_all:
      break

  _raw_write(config_file, data)

def _undo(values, contexts):
  if len(values) > 1:
    return LOGGER.error('"config undo" takes at most one argument.')

  config_file, data = _get_raw_file()
  if values:
    v = values[0]
    if v == 'all':
      length = 0
    elif v == 'top':
      length = 1
    else:
      return LOGGER.error('Don\'t understand "config undo %s"', v)
  else:
    length = max(len(data) - 1, 0)

  if _LOCAL_CHANGES:
    _REDO_STACK.push([True, Yaml.encode_one(_LOCAL_CHANGES)])
    _LOCAL_CHANGES.clear()
    if not values:
      LOGGER.info('Cleared local changes.')
      return

  for d in parts[length:]:
    _REDO_STACK.push([False, d])
  _raw_write(config_file, data[0:length])
