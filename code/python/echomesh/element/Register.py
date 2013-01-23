from __future__ import absolute_import, division, print_function, unicode_literals

ELEMENT_MAKERS = {}

def register(element_maker, name=None):
  name = (name or element_maker.__name__).lower()
  old_maker = ELEMENT_MAKERS.get(name, None)
  if old_maker is not element_maker:
    if old_maker:
      raise Exception('Duplicate function name %s' % name)
    ELEMENT_MAKERS[name] = element_maker
