from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import CommandFile
from echomesh.base import Join
from echomesh.base import Yaml
from echomesh.element import Element
from echomesh.util import Dict
from echomesh.util import Log
from echomesh.util.Registry import Registry

LOGGER = Log.logger(__name__)

_REGISTRY = Registry(name='element', class_path='echomesh.element')

def register(classname, name=None):
  _REGISTRY.register(classname, (name or classname).lower())

register('Audio')
register('Handler')
register('Image')
register('Loop')
register('Print')
register('Repeat')
register('Root')
register('Pattern')
register('Schedule')
register('Sequence')
register('Select')
register('Speak')
register('Twitter')

def _resolve_extensions(data):
  extensions = set()
  datas = [data]

  while True:
    extension = data.get('inherit')
    if not extension:
      break

    try:
      extension, data = CommandFile.load_resolve('score', extension)
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

NOT_ACCESSED_ERROR = """\
In an element of type "%s" loaded from "%s", \
the following properties were ignored because they were not understood:

  %s"""

NOT_ACCESSED_ERROR_SINGLE = """\
In an element of type "%s" loaded from "%s", \
the following property was ignored because it was not understood:

  %s"""

def make_one(parent, description):
  description = Dict.Access(_resolve_extensions(description))
  t = description.get('type', '').lower()
  if not t:
    raise Exception('No type field in element %s' % description)

  element_class = _REGISTRY.function(t)
  if not element_class:
    _REGISTRY.dump()
    raise Exception('No element class for type %s' % t)

  element = element_class(parent, description)
  not_accessed = description.not_accessed()
  if not_accessed:
    score = element.get_root().get_property('score') or ''
    if len(not_accessed) == 1:
      error = NOT_ACCESSED_ERROR_SINGLE
    else:
      error = NOT_ACCESSED_ERROR
    LOGGER.error(error, t, score, Join.join_words(not_accessed))

  return element

def make(parent, descriptions):
  if not isinstance(descriptions, (list, tuple)):
    descriptions = [descriptions]
  return [make_one(parent, d) for d in descriptions]
