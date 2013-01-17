from __future__ import absolute_import, division, print_function, unicode_literal

from echomesh.config import CommandFile
from echomesh.util import Log

LOGGER = Log.logger(__name__)

def raw_load(*path):
  f = CommandFile.resolve(*path)
  if f:
    data = File.yaml_load_all(f)
    if data:
      return data
    LOGGER.error("Couldn't read Yaml from file %s", '/'.join(path))
  else:
    LOGGER.error("Couldn't find file %s", '/'.join(path))


def load(*path):
  extension = path
  datas = []
  extensions = set()
  while True:
    if extension in extensions:
      LOGGER.error('Infinite circular extension for %s', extend)
      break
    data = raw_load(*extension)
    if not data:
      break
    datas.append(data)
    extensions.add(extension)

    extension = data.get('extends', None)
    if not extension:
      break
    if isinstance(extension, str):
      extension = (extension, )
    else:
      extension = tuple(extension)

  result = {}
  for data in reversed(datas):
    result.update(data)
  return result
