from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util.registry.Module import register_parent
from echomesh.output.OutputCache import OutputCache

REGISTRY = register_parent(
  __name__,
  'Bidirectional',
  'Offset',
  'Output',
  'Map',
  'Spi',
  'Test',
  'Visualizer',
)

OUTPUT_CACHE = OutputCache()

def make_output(data):
  if isinstance(data, dict):
    return REGISTRY.make_from_description(data, default_type='output')
  else:
    return OUTPUT_CACHE.get_output(data)

def pause_outputs():
  from echomesh.output.Output import pause_outputs
  pause_outputs()
