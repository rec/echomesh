from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Args
from echomesh.base import CommandFile
from echomesh.base import GetPrefix
from echomesh.base import Merge
from echomesh.base import Yaml

def merge_config():
  return _merge_assignments(_merge_file_config())

def _merge_assignments(config):
  for address, value in _get_assignments():
    try:
      _merge_assignment(config, address, value)
    except Exception as e:
      _add_exception_suffix(e, 'while merging', address, '=', value)
  return config

def _merge_assignment(table, address, value):
  t = table
  for i, field in enumerate(address):
    if i < len(address) - 1:
      t = GetPrefix.get_prefix_and_match(t, field, 'merge_config')[1]
    else:
      t[field] = value
      print('%s=%s' % (':'.join(address), value))

def _get_assignments():
  assignments = Args.ASSIGNMENT_ARGS
  if Args.YAML_ARGS:
    arg = ' '.join(Args.YAML_ARGS)
    try:
      arg_config = Yaml.decode(arg)
    except Exception as e:
      print('%s while decoding command line arguments', e)
    else:
      assignments += table_to_parts(arg_config)

  return assignments

def _merge_file_config():
  config = None

  for f in reversed(CommandFile.expand('config.yml')):
    try:
      file_configs = Yaml.read(f)
    except Exception as e:
      _add_exception_suffix(e, 'while reading config file', f)
      raise

    for cfg in file_configs:
      if config is None:
        assert cfg, "Unable to read default file %s" % f
        config = cfg
      else:
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
  suffix = ' '.join(suffixes)
  e.args = tuple(a + suffix for a in e.args)
