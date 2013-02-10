from __future__ import absolute_import, division, print_function, unicode_literals

import itertools

from echomesh.base import CommandFile
from echomesh.base import Yaml
from echomesh.base import Merge

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
      _add_exception_suffix(e, message, 'parsing', item)
      raise

def merge(args):
  files = reversed(CommandFile.expand('config.yml'))
  file_iter = _parse(files, Yaml.read_all, 'config file')
  args = (a for a in args if a[0] in '{[')
  arg_iter = _parse(args, Yaml.decode_all, 'command line argument')
  config = None

  for cfg, item, message in itertools.chain(file_iter, arg_iter):
    if config is None:
      assert cfg, "Unable to read default %s %s" % (message, item)
      config = cfg
    else:
      try:
        Merge.merge(config, cfg)
      except Exception as e:
        _add_exception_suffix(e, message, 'merging', item)
  return config
