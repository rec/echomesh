from __future__ import absolute_import, division, print_function, unicode_literals

import os.path

from echomesh.base import Config
from echomesh.base import Enum
from echomesh.base import Path
from echomesh.base import Platform
from echomesh.expression import Units

CLIENT_NAME = 'echomesh-client'
COMMAND = os.path.join(Path.BINARY_PATH, CLIENT_NAME)

ControlType = Enum.Enum('FILE', 'SOCKET', 'TERMINAL')

def make_command():
  parts = []
  if Platform.IS_LINUX:
    parts.append('sudo')
  parts.append(COMMAND)

  config = Config.get('network', 'client')
  type_name, client_type = ControlType.get(config['type'])
  parts.append(type_name.lower())

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

