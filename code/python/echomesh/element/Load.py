from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.element import Error
from echomesh.element import REGISTRY
from echomesh.element.ResolveExtensions import resolve_extensions
from echomesh.util.dict.Access import Access
from echomesh.util import Log

LOGGER = Log.logger(__name__)

def load_one_element(parent, description):
  description = Access(resolve_extensions(description))
  t = description.get('type', '').lower()
  if not t:
    raise Exception('No type field in element %s' % description)

  element = REGISTRY.function(t)(parent, description)
  Error.not_accessed(LOGGER, element, description.not_accessed(), t)
  return element

def load_elements(parent, descriptions):
  if not isinstance(descriptions, (list, tuple)):
    descriptions = [descriptions]
  return [load_one_element(parent, d) for d in descriptions]


