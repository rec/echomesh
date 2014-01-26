from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import DataFile
from echomesh.pattern import REGISTRY

def make_pattern(element, name, description, is_top_level=True):
  entry = REGISTRY.get_from_description(description)

  # TODO: Get rid of this or somehow fix this.
  if is_top_level:
    name = '%s:%s' % (name, entry.name)

  return entry.function(description, element, name)

def make_pattern_from_file(element, name):
  desc = DataFile.load('pattern', name)[0]
  return make_pattern(element, name, desc)
