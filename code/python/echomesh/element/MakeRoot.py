from __future__ import absolute_import, division, print_function, unicode_literals

import os.path

from echomesh.base import DataFile
from echomesh.base import Yaml
from echomesh.element.Root import Root
from echomesh.util import Log
from echomesh.util.string import UniqueName

LOGGER = Log.logger(__name__)

def make_root(score_names, table):
  result = {}
  for score_file, name in score_names:
    resolved_file = DataFile.resolve('score', score_file)
    if not resolved_file:
      LOGGER.error('No such score file: "%s".',
                   DataFile.base_file('score', score_file))
      continue
    elements = Yaml.read(resolved_file)
    description = {'elements': elements, 'type': 'score'}
    parts = resolved_file.split('/')
    final_file = '/'.join([parts[1]] + parts[3:])

    try:
      element = Root(description, final_file)
    except Exception:
      LOGGER.error("\nError when reading score file %s", score_file)
      continue

    name = os.path.splitext(name or score_file)[0]
    name = UniqueName.unique_name(name, table)
    result[name] = element
    element.name = name

  return result
