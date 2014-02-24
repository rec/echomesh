from echomesh.util.registry.Module import register as _register

REGISTRY = _register(
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
