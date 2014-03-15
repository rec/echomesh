from echomesh.util.registry.Module import register_module as _register_module

REGISTRY = _register_module(
  __name__,
  'Event',
  'Config',
  'Peer',
  'Transfer',
  )
