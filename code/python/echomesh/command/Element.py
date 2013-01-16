from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.config import CommandFile
from echomesh.util import Log

LOGGER = Log.logger(__name__)

def load(element):
  filename = element.get('filename', None)
  if filename:
    data = CommandFile.load('element', filename)
    if data:
      return data
    LOGGER.error("Couldn't load element file %s", filename)

  return element

def validate(element, functions):
  ok = True
  for command in element.get('mapping', {}).itervalues():
    cmd = command.get('function', None)
    if cmd not in functions:
      ok = False
      LOGGER.error("Didn't understand command %s in element %s", cmd, element)

  return ok
