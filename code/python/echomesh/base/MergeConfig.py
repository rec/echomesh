from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import sys

from echomesh.base import Args
from echomesh.base import CommandFile
from echomesh.base import GetPrefix
from echomesh.base import Merge
from echomesh.base import Yaml

_ARGUMENT_ERROR = """
ERROR: Didn't understand arguments to echomesh: "%s".

echomesh needs to be called with arguments looking like "name=value".

Examples:
  echomesh
  echomesh debug=true
  echomesh audio.input.enable=false light.enable=false
"""

_ASSIGNMENT_ERROR = """
ERROR: couldn't assign a variable from: "%s".

Variable assignments look like "name=value" and you can have more than one
per line.

Examples:
  debug=true
  audio.input.enable=false light.enable=false
"""

class MergeConfig(object):
  def __init__(self):
    self.read()

  def read(self):
    files = _read_files()
    self.file_configs = self._read_file_configs()
    self.arg_config = self._assignment_to_config(sys.argv[1:], _ARGUMENT_ERROR)
    return self.recalculate()

  def assign(self, args, index=-1):
    configs = self.file_configs[index]  # default is 'master'
    while len(configs) < 3:
      configs.append[{}]
    Merge.merge(configs[2], self._assignment_to_config(args, _ASSIGNMENT_ERROR))
    return self.recalculate()

  def assignments(self, index=-1):
    assigned = self.file_configs[index]
    return (len(assigned) > 2 and GetPrefix.leafs(assigned[2])) or {}

  def recalculate(self):
    self.config = {}
    changed = {}
    for _, configs in self.file_configs:
      Merge.merge(self.config, *configs)
      Merge.merge(changed, *configs[2:])

    arg = copy.deepcopy(self.arg_config)
    Merge.merge(self.config, Merge.difference_strict(arg, changed))

    return self.config

  def _read_file_configs(self):
    self.file_configs = []
    base_config = None

    for f in reversed(CommandFile.expand('config.yml')):
      configs = Yaml.read(f, 'config')
      for c in configs:
        if base_config:
          Merge.merge_for_config(base_config, c)
        else:
          base_config = copy.deepcopy(c)
      self.file_configs.append([configs, f])

  def _assignment_to_config(self, args, error):
    arg = ' '.join(args)
    config = {}
    try:
      for address, value in Args.split(arg):
        GetPrefix.set_accessor(address, value, self.config, config,
                               unmapped_names=Merge.CONFIG_EXCEPTIONS,
                               allow_prefixes=True)
      return config

    except Exception as e:
      e.arg = arg
      raise
