from echomesh.util.registry.Module import register as _register
from echomesh.base import DataFile as _DataFile

_REGISTRY = _register(
  __name__,
  'Choose',
  'Concatenate',
  'Fade',
  'Inject',
  'Insert',
  'Mirror',
  'Spread',
  'Reverse',
)

def make_pattern(element, description, name=None, patterns=None):
  if not isinstance(description, dict):
    name = description
    pattern = (patterns or {}).get(name)
    if pattern:
      return pattern
    description = _DataFile.load('pattern', name)[0]

  entry = _REGISTRY.get_from_description(description)
  name = name + entry.name if name else entry.name
  return entry.function(description, element, name)


