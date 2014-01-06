from __future__ import absolute_import, division, print_function, unicode_literals

def _make_make_output():
  from echomesh.util.registry.Module import register
  from echomesh.output.OutputCache import OutputCache

  registry = register(
    __name__,
    'Bidirectional',
    'Offset',
    'Output',
    'Map',
    'Test',
    'Visualizer',
  )

  output_cache = OutputCache()

  def make_output(data):
    if isinstance(data, dict):
      return registry.make_from_description(data, default_type='output')
    else:
      return output_cache.add_output(data)

  return make_output, output_cache.pause

make_output, pause_outputs = _make_make_output()
