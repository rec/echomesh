from echomesh.util.registry.Module import register as _register

_ARGS = (
  'Audio',
  'Handler',
  'Image',
  'Loop',
  'Print',
  'Repeat',
  'Root',
  'Pattern',
  'Schedule',
  'Sequence',
  'Select',
  'Speak',
  'Twitter',
)

_register(__name__, *_ARGS)
