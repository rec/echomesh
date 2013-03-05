from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import GetPrefix
from echomesh.base import Args
from echomesh.base import CommandFile
from echomesh.base import Merge
from echomesh.base import Path
from echomesh.base import Yaml

def merge_config():
  config = Yaml.read(CommandFile.config_file('default'))[0]
  assert config, 'Unable to read default config file'

  return _merge_assignments(_merge_file_config(config), _get_assignments())

def _merge_assignments(config, assignments):
  for address, value in assignments:
    try:
      cfg = config
      for i, field in enumerate(address):
        if i < len(address) - 1:
          cfg = GetPrefix.get_prefix_and_match(cfg, field, 'merge_config')[1]
        else:
          cfg[field] = value
          print('%s=%s' % ('.'.join(address), value))

    except Exception as e:
      _add_exception_suffix(e, 'while merging', '.'.join(address),
                            '=', str(value))
      raise
  return config


def _get_assignments():
  assignments = []
  for address, value in Args.ASSIGNMENT_ARGS:
    try:
      value = Yaml.decode_one(value)
    except Exception as e:
      print('ERROR: %s while decoding command line arguments:' % str(e),
            address, value)
    else:
      assignments.append([address, value])

  if Args.YAML_ARGS:
    arg = ' '.join(Args.YAML_ARGS)
    try:
      arg_config = Yaml.decode_one(arg)
    except Exception as e:
      print('%s while decoding command line arguments', e)
    else:
      assignments += table_to_parts(arg_config)

  # Get the project field out of the command line if it exists,
  # before we get any file past the default configuration.
  for address, value in assignments:
    if len(address) == 1 and 'project'.startswith(address[0]):
      Path.set_project_path(value, show_error=True)
      CommandFile.compute_command_path()
      break
  else:
    Path.set_project_path(show_error=True)

  return assignments

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

def table_to_parts(table):
  parts = []
  def to_parts(t, prefix):
    for k, v in t.iteritems():
      if isinstance(v, dict):
        to_parts(v, prefix + [k])
      else:
        parts.append([prefix + [k], v])
  to_parts(table, [])
  return parts

def _add_exception_suffix(e, *suffixes):
  # TODO: use traceback!!
  suffix = ' '.join(suffixes)
  e.args = tuple(a + suffix for a in e.args)
