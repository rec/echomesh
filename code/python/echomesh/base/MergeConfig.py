from __future__ import absolute_import, division, print_function, unicode_literals

import itertools

from echomesh.base import Args
from echomesh.base import CommandFile
from echomesh.base import Merge
from echomesh.base import Yaml

def merge_config():
  config = None

  files = reversed(CommandFile.expand('config.yml'))
  file_iter = _parse(files, Yaml.read, 'config file')
  arg_iter = _parse(Args.YAML_ARGS, Yaml.decode, 'command line argument')

  for cfg, item, message in itertools.chain(file_iter, arg_iter):
    if config is None:
      assert cfg, "Unable to read default %s %s" % (message, item)
      config = cfg
    else:
      try:
        config = Merge.merge_for_config(config, cfg)
      except Exception as e:
        _add_exception_suffix(e, ' while merging', message, item)
        raise


  return config

def merge_config2():
  config = None

  for f in reversed(CommandFile.expand('config.yml')):
    try:
      cfg = Yaml.read(f)
    except Exception as e:
      _add_exception_suffix(e, 'while reading config file', f)
      raise

    if config is None:
      assert cfg, "Unable to read default file %s" % f
      config = cfg
    else:
      try:
        config = Merge.merge_for_config(config, cfg)
      except Exception as e:
        _add_exception_suffix(e, ' while merging config file', f)
        raise

  if Args.YAML_ARGS:
    arg = ' '.join(Args.YAML_ARGS)
    try:
      arg_config = Yaml.decode(arg)
    except Exception as e:
      _add_exception_suffix(e, 'while decoding command line arguments', arg)
      raise

  if Args.ASSIGNMENT_ARGS:
    pass

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

def _merge_assignment(table, address, value, error_name='merge_assignment'):
  t = table
  for i, field in enumerate(address):
    if i < len(address) - 1:
      t = GetPrefix.get_prefix_and_match(t, field, error_name)[1]
    else:
      t[field] = value

def get_args():
  if args and _is_yaml(ARGS[0]):
    line = ' '.join(ARGS).strip()

  if _is_yaml(line):
    pass
  else:
    pass

def _add_exception_suffix(e, *suffixes):
  suffix = ' '.join(suffixes)
  e.args = tuple(a + suffix for a in e.args)

def _parse(items, parser, message):
  for item in items:
    try:
      for cfg in parser(item):
        if cfg:
          yield cfg, item, message
    except Exception as e:
      _add_exception_suffix(e, ' while parsing', message, item)
      raise
