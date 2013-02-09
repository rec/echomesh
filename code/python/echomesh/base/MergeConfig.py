from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import CommandFile
from echomesh.base import File
from echomesh.base import Merge

def _add_exception_suffix(e, suffix):
  e.args = tuple(a + suffix for a in e.args)

def _merge_level_files():
  # Merge configuration files from the command directory hierarchy.
  config = None
  for f in reversed(CommandFile.expand('config.yml')):
    try:
      cfg = File.yaml_load(f)
    except:
      _add_exception_suffix(e, ' loading configuration file %s' % f)

    if config is None:
      assert cfg, "Unabled to read default config file %s" % f
      config = cfg
    else:
      try:
        Merge.merge(config, cfg)
      except Exception as e:
        _add_exception_suffix(e, ' merging configuration file %s' % f)
        raise
  return config

def _merge_command_line_arguments(args, config):
  # Merge in command line arguments.
  for i, arg in enumerate(args):
    if arg and arg[0] == '{':
      try:
        cfgs = File.yaml_load_stream(arg)
      except:
        _add_exception_suffix(e, ' parsing command line argument %d: "%s"' %
                              (i, arg))
        raise

      try:
        Merge.merge_all(config, *cfgs)
      except Exception as e:
        _add_exception_suffix(e, ' merging command line argument %d: "%s"' %
                              (i, arg))
        raise
  return config

def merge(args):
  return _merge_command_line_arguments(args, _merge_level_files())
