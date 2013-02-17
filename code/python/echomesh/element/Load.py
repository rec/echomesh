from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import CommandFile
from echomesh.base import Yaml
from echomesh.element import Element
from echomesh.util import Log

LOGGER = Log.logger(__name__)

def _resolve_extensions(data):
  extensions = set()
  datas = [data]

  while True:
    extension = data.get('extends')
    if not extension:
      break
    extension = Yaml.filename(extension)

    if extension in extensions:
      raise Exception('Infinite circular extension for %s' % extension)

    try:
      data = CommandFile.load('score', extension)
    except Exception as e:
      raise Exception("Couldn't find extension for %s: %s" % (extension, str(e)))

    if len(data) > 1:
      LOGGER.error("More than one element in extension %s", extension)
    data = data[0]

    datas.append(data)
    extensions.add(extension)

  result = {}
  for data in reversed(datas):
    result.update(data)
  if extensions:
    del result['extends']

  return result

def make_one(parent, desc):
  desc = _resolve_extensions(desc)
  t = desc.get('type', '').lower()
  if not t:
    raise Exception('No type field in element %s' % desc)

  maker = Element.get_element_by_name(t)
  if not maker:
    Element._REGISTRY.dump()
    raise Exception('No element maker for type %s' % t)

  return maker(parent, desc)

def make(parent, descriptions):
  return [make_one(parent, d) for d in descriptions]
