from __future__ import absolute_import, division, print_function, unicode_literals

import os.path

from echomesh.base import Config
from echomesh.base import Enum
from echomesh.base import Path
from echomesh.base import Platform
from echomesh.util import Log
from echomesh.expression import Units

LOGGER = Log.logger(__name__)

COMMAND = os.path.join(Path.BINARY_PATH, 'echomesh')

ControlType = Enum.Enum('FILE', 'SOCKET', 'TERMINAL')

def make_command():
  parts = []
  if Platform.IS_LINUX:
    parts.append('sudo')
  parts.append(COMMAND)

  config = Config.get('network', 'client')
  client_type = ControlType.get(config['type'])[1]

  if client_type == ControlType.FILE:
    parts.append(config['input_file'])

  elif client_type == ControlType.SOCKET:
    parts.append(config['host_name'])
    parts.append(str(config['port']))
    timeout = Units.convert(config['timeout'])
    parts.append(str(timeout))
    parts.append(str(config['buffer_size']))

  elif client_type != ControlType.TERMINAL:
    raise Exception('Can\'t understand type %s' % client_type)

  return client_type, parts

