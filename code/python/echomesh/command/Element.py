from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.config import Loader
from echomesh.util import Log
from echomesh.util import Merge

LOGGER = Log.logger(__name__)

def make(desc, parent, makers):
  desc = Loader.load(desc)
  t = desc.get('type', None)
  if not t:
    LOGGER.error('No type field in element %s', desc)
  else:
    maker = makers.get(t, None)
    if not maker:
      LOGGER.error('No element maker for type %s', t)
    else:
      return maker(parent, desc)

# Probably obsolete.
def classify(element_descs, makers, parent):
  elements_by_type = {}

  for desc in element_descs:
    element = make(desc, parent, makers)
    elements_by_subtype = elements_by_type.get(t, None)
    if elements_by_subtype is None:
      elements_by_subtype = {}
      elements_by_type[t] = elements_by_subtype

    subtype = desc.get('subtype', t)
    subelements = elements_by_subtype.get(subtype, None)
    if subelements is None:
      subelements = []
      elements_by_subtype[subtype] = subelements

    subelements.append(element)

  return elements_by_type

