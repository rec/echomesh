from __future__ import absolute_import, division, print_function, unicode_literals

import os.path

from echomesh.base import Config
from echomesh.base import Enum
from echomesh.base import Path
from echomesh.base import Platform
from echomesh.expression import Units

CLIENT_NAME = 'echomesh-client'
COMMAND = os.path.join(Path.BINARY_PATH, CLIENT_NAME)

def make_command():
  parts = []
  if Platform.IS_LINUX:
    parts.append('sudo')

  config = Config.get('network', 'client')

  parts.append(config['binary'] or COMMAND)
  parts.append(config['host_name'])
  parts.append(str(config['port']))
  timeout = Units.convert(config['timeout'])
  parts.append(str(timeout))
  parts.append(str(config['buffer_size']))

  return parts

