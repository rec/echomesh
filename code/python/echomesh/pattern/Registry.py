from echomesh.util.registry.Module import register
from echomesh.base import DataFile

REGISTRY = register(
  __name__,
  'Animation',
  'Choose',
  'Columns',
  'Concatenate',
  'Expand',
  'Fade',
  'Image',
  'Inject',
  'Insert',
  'List',
  'Mirror',
  'Scroll',
  'Spread',
  'Text',
  'Tile',
  'Reverse',
)

def make_pattern(element, description, name=None, patterns=None):
    if not isinstance(description, dict):
        name = description
        pattern = (patterns or {}).get(name)
        if pattern:
            return pattern
        description = DataFile.load('pattern', name)[0]

    entry = REGISTRY.get_from_description(description)
    name = name + entry.name if name else entry.name
    return entry.function(description, element, name)
