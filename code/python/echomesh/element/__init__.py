from echomesh.util.registry.Module import register_module as _register_module

REGISTRY = _register_module(
  __name__,
  'Audio',
  'Execute',
  'Handler',
  'Image',
  'Loop',
  'Movie',
  'Print',
  'Repeat',
  'Root',
  ('Pattern', 'PatternElement'),
  'Schedule',
  'Sequence',
  'Select',
  'Snapshot',
  'Speak',
  'Twitter',
  'Video',
)
