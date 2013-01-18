from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.config import CommandFile
from echomesh.util import Log

LOGGER = Log.logger(__name__)

def _load(*path):
  f = CommandFile.resolve(*path)
  if f:
    data = File.yaml_load_all(f)
    if data:
      return data
    LOGGER.error("Couldn't read Yaml from file %s", '/'.join(path))
  else:
    LOGGER.error("Couldn't find file %s", '/'.join(path))
  return []

def resolve_extensions(data):
  extensions = set()
  datas = [data]
  while True:
    extension = data.get('extends', None)
    if not extension:
      break

    if extension in extensions:
      LOGGER.error('Infinite circular extension for %s', extend)
      break

    data = _load(extension)
    if not data:
      LOGGER.error("Couldn't find extension for %s", extend)
      break

    if len(data) > 1:
      LOGGER.error("More than one element in extension %s", extend)

    datas.append(data[0])
    extensions.add(extension)

  result = {}
  for data in reversed(datas):
    result.update(data)
  del result['extends']
  return result

def make(parent, descriptions, makers):
  for desc in descriptions:
    desc = resolve_extensions(desc)
    t = desc.get('type', None)
    if not t:
      LOGGER.error('No type field in element %s', desc)
    else:
      maker = makers.get(t, None)
      if not maker:
        LOGGER.error('No element maker for type %s', t)
      else:
        yield maker(parent, desc)

def load_and_make(parent, filename, makers):
  return make(parent, _load(filename), makers)
