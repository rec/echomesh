from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import six
import sys

from echomesh.base import Args
from echomesh.base import CommandFile
from echomesh.base import GetPrefix
from echomesh.base import Merge
from echomesh.base import Path
from echomesh.base import Yaml

LOCAL_CHANGES = {}
ARGUMENT_CHANGES = {}

_ARGUMENT_ERROR = """
ERROR: Didn't understand arguments to echomesh: "%s".

echomesh needs to be called with arguments looking like "name=value".

Examples:
  echomesh
  echomesh debug=true
  echomesh audio.input.enable=false light.enable=false
"""

def reconfigure():
  config = CommandFile.read_config('default')
  assert config, 'Unable to read default config file'

  args = _get_args()
  _set_project_path(args)
  config = _merge_file_config(config)
  merge_assignments(config, args, save=False)

  return config

def merge_assignments(config, assignments, changes=None):
  changes = changes or LOCAL_CHANGES
  def _merge(address, value):
    path = []
    values = []
    for i, field in enumerate(address.split('.')):
      key, val = GetPrefix.get_prefix(config, field)
      path.append(key)
      if i == len(address) - 1:
        changes[key] = val
        config[key] = copy.deepcopy(val)
        return [path, value]
      else:
        config = val
        changes = changes.setdefault(key, {})
  return [_merge(a, v) for a, v in assignments]


def _get_args():
  arg = ' '.join(sys.argv[1:])
  try:
    return Args.split(arg)
  except:
    print(_ARGUMENT_ERROR % arg)
    raise


def _is_autostart(args):
  for address, value in args:
    if 'autostart'.startswith(address):
      return True

def _set_project_path(args):
  prompt = not _is_autostart(args)

  # Get the project field out of the command line if it exists,
  # before we get any file past the default configuration.
  for address, value in args:
    if 'project'.startswith(address):
      Path.set_project_path(value, show_error=True, prompt=prompt)
      CommandFile.compute_command_path()
      break
  else:
    Path.set_project_path(show_error=True)

def _merge_file_config(config):
  for f in list(reversed(CommandFile.expand('config.yml')))[1:]:
    try:
      file_configs = Yaml.read(f)
    except Exception as e:
      _add_exception_suffix(e, 'while reading config file', f)
      raise

    for cfg in file_configs:
      try:
        config = Merge.merge_for_config(config, cfg)
      except Exception as e:
        _add_exception_suffix(e, ' while merging config file', f)
        raise
  return config

def _add_exception_suffix(e, *suffixes):
  # TODO: use traceback.
  suffix = ' '.join(suffixes)
  e.args = tuple(a + suffix for a in e.args)
