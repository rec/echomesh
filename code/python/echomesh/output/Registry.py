from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util.registry.Module import register
from echomesh.output.OutputCache import OutputCache

REGISTRY = register(
  '.'.join(__name__.split('.')[:-1]),
  'Bidirectional',
  'Offset',
  'Output',
  'Map',
  'Test',
  'Visualizer',
)

OUTPUT_CACHE = OutputCache()

def make_output(data):
  if isinstance(data, dict):
    return REGISTRY.make_from_description(data, default_type='output')
  else:
    return OUTPUT_CACHE.get_output(data)

pause_outputs = OUTPUT_CACHE.pause
