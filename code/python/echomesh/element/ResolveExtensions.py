from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import DataFile
from echomesh.util import Log

LOGGER = Log.logger(__name__)

def resolve_extensions(data):
  extensions = set()
  datas = [data]

  while True:
    extension = data.get('inherit')
    if not extension:
      break

    try:
      extension, data = DataFile.load_resolve('score', extension)
    except Exception as e:
      raise Exception("Couldn't find extension for %s: %s" % (extension, str(e)))

    if extension in extensions:
      raise Exception('Infinite circular extension for %s' % extension)

    if len(data) > 1:
      LOGGER.error("More than one element in extension %s", extension)
    data = data[0]

    datas.append(data)
    extensions.add(extension)

  result = {}
  for data in reversed(datas):
    result.update(data)
  if extensions:
    del result['inherit']

  return result
