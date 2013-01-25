from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import CommandFile
from echomesh.base import File
from echomesh.element import Element
from echomesh.util import Log

LOGGER = Log.logger(__name__)

def load(*path):
  data, error = CommandFile.load_with_error(*path)
  if error:
    LOGGER.error(error)
  return data

def _resolve_extensions(data):
  extensions = set()
  datas = [data]

  while True:
    extension = data.get('extends', None)
    if not extension:
      break

    if extension in extensions:
      raise Exception('Infinite circular extension for %s' % extend)

    data = load(extension)
    if not data:
      raise Exception("Couldn't find extension for %s" % extend)

    if len(data) > 1:
      LOGGER.error("More than one element in extension %s", extend)

    datas.append(data[0])
    extensions.add(extension)

  result = {}
  for data in reversed(datas):
    result.update(data)
  if extensions:
    del result['extends']
  return result

def make_one(parent, desc):
  desc = _resolve_extensions(desc)
  t = desc.get('type', None).lower()
  if not t:
    raise Exception('No type field in element %s' % desc)

  maker = Element.get_element_by_name(t, None)
  if not maker:
    raise Exception('No element maker for type %s' % t)

  return maker(parent, desc)

def make(parent, descriptions):
  return [make_one(parent, d) for d in descriptions]
