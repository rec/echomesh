from echomesh.util.registry.Module import register

_REGISTRY = None

def registry():
  global _REGISTRY
  if not _REGISTRY:
    _REGISTRY = register(
      __name__,
      'Alias',
      'Broadcast',
      'Transfer',
      'Save'
    )
  return _REGISTRY
