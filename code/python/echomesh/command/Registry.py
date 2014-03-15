from echomesh.util.registry.Module import register_parent

_REGISTRY = None

def registry():
  global _REGISTRY
  if not _REGISTRY:
    _REGISTRY = register_parent(
      __name__,
      'Alias',
      'Broadcast',
      'Transfer',
      'Save'
    )
  return _REGISTRY
