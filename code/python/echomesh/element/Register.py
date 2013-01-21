from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Log
from echomesh.element import Audio, Image, Print, Random, Sequence

LOGGER = Log.logger(__name__)

ELEMENT_MAKERS = {}

def register(element_maker, name=None):
  name = (name or element_maker.__name__).lower()
  old_maker = ELEMENT_MAKERS.get(name, None)
  if old_maker is not element_maker:
    if old_maker:
      raise Exception('Duplicate function name %s' % name)
    ELEMENT_MAKERS[name] = element_maker

register(Audio)
register(Image)
register(Print)
register(Random)
register(Sequence)
