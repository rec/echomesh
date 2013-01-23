from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import CommandFile
from echomesh.base import File
from echomesh.element import Register
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
      LOGGER.error('Infinite circular extension for %s', extend)
      break

    data = load(extension)
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
  if extensions:
    del result['extends']
  return result

def _make_element(parent, desc):
  desc = _resolve_extensions(desc)
  t = desc.get('type', None)
  if not t:
    LOGGER.error('No type field in element %s', desc)
  else:
    maker = Register.ELEMENT_MAKERS.get(t, None)
    if not maker:
      LOGGER.error('No element maker for type %s', t)
    else:
      return maker(parent, desc)

def make(parent, *descriptions):
  elements = []
  for desc in descriptions:
    try:
      element = _make_element(parent, desc)
    except:
      LOGGER.error("Couldn't read element from description %s", desc)
      import traceback
      LOGGER.error(traceback.format_exc())
    else:
      if element:
        elements.append(element)

  return elements

