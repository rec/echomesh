from __future__ import absolute_import, division, print_function, unicode_literals

import itertools

from echomesh.base import CommandFile
from echomesh.base import Merge
from echomesh.base import Path
from echomesh.base import Yaml

def _add_exception_suffix(e, *suffixes):
  suffix = ' '.join(suffixes)
  e.args = tuple(a + suffix for a in e.args)

def _parse(items, parser, message):
  for item in items:
    try:
      pi = parser(item)
      if pi is None:
        print(parser, item)
      for cfg in parser(item):
        if cfg:
          yield cfg, item, message
    except Exception as e:
      _add_exception_suffix(e, message, 'parsing', item)
      raise

def merge():
  args = Path.yaml_args()
  config = None

  files = reversed(CommandFile.expand('config.yml'))
  file_iter = _parse(files, Yaml.read, 'config file')
  arg_iter = _parse(args, Yaml.decode, 'command line argument')

  for cfg, item, message in itertools.chain(file_iter, arg_iter):
    if config is None:
      assert cfg, "Unable to read default %s %s" % (message, item)
      config = cfg
    else:
      try:
        Merge.merge_strict(config, cfg)
      except Exception as e:
        _add_exception_suffix(e, message, 'merging', item)
  return config
