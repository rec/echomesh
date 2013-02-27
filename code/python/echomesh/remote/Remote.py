from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.remote import Register, Routing, System, Transfer
from echomesh.util import Log

LOGGER = Log.logger(__name__)

def execute(echomesh, type=None, **data):
  try:
    if not type:
      raise Exception("No type in data %s" % data)
    function = Register.get(type)
    if not function:
      raise Exception("Didn't understand data type %s" % type)

    return function(echomesh, type=type, **data)

  except Exception as e:
    LOGGER.error()
    raise
