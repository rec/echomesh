from __future__ import absolute_import, division, print_function, unicode_literals

import six

from echomesh.base import Args
from echomesh.base import CommandFile
from echomesh.base import GetPrefix
from echomesh.base import Merge
from echomesh.base import Path
from echomesh.base import Yaml

LOCAL_CHANGES = {}

def merge_config():
  config = Merge.merge(*Yaml.read(CommandFile.config_file('default')))
  assert config, 'Unable to read default config file'

  _set_project_path()
  config = _merge_file_config(config)
  merge_assignments(config, Args.ARGS)
  return config

def merge_assignments(config, assignments):
  results = []
  for address, value in assignments:
    try:
      cfg, changes = config, LOCAL_CHANGES
      path = []
      for i, field in enumerate(address):
        k, v = GetPrefix.get_prefix(cfg, field)
        path.append(k)
        if i < len(address) - 1:
          cfg = v
          changes = changes.setdefault(k, {})
        else:
          cfg[k] = changes[k] = value
          results.append([path, value])

    except GetPrefix.PrefixException:
      raise Exception('Configuration variable "%s" doesn\'t exist' %
                      '.'.join(address))

  return results

def _set_project_path():
  # First, find out if we're autostarting.
  autostart = False
  for address, value in Args.ARGS:
    if len(address) == 1 and 'autostart'.startswith(address[0]):
      autostart = True
      break

  # Get the project field out of the command line if it exists,
  # before we get any file past the default configuration.
  for address, value in Args.ARGS:
    if len(address) == 1 and 'project'.startswith(address[0]):
      Path.set_project_path(value, show_error=True, prompt=not autostart)
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
