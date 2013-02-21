from __future__ import absolute_import, division, print_function, unicode_literals

import os
import os.path

from echomesh.base import Path
from echomesh.base import Yaml
from echomesh.command import Register
from echomesh.util import Join
from echomesh.util import Log

LOGGER = Log.logger(__name__)

TRANSFER_PROMPT =  """
Are you sure you want to transfer all command files over to all echomesh nodes
on this network, replacing whatever is there (y/N)?
"""

def transfer(echomesh, *args):
  if not args:
    LOGGER.print(TRANSFER_PROMPT)
    if not raw_input().lower().startswith('y'):
      LOGGER.print('Transfer cancelled.')
      return
    args = ['*']
  if '*' in args or '.' in args:
    args = ['']

  files = set()
  directories = set()
  for arg in args:
    f = os.path.join(Path.COMMAND_PATH, arg)
    if not os.path.exists(f):
      raise Exception("Command file %s doesn't exist.", f)
    walk = os.walk(f)
    if walk:
      directories.add(arg)
      for root, dirs, fs in walk:
        for ffs in fs:
          if ffs.endswith('.yml'):
            files.add(os.path.join(Path.COMMAND_PATH, root, ffs))
      LOGGER.debug('Adding directory %s', arg)
    else:
      LOGGER.debug('Adding file %s', arg)
      files.add(f)

  files_table = {}
  files = sorted(files)
  for f in files:
    stat = os.stat(f)
    files_table[f] = {'contents': Yaml.read(f),
                      'atime': stat.st_atime,
                      'mtime': stat.st_mtime}

  s = '' if len(files) is 1 else 's'
  LOGGER.print('Transferred %d file%s.' % (len(files), s))
  echomesh.send(type='transfer',
                directories=sorted(directories),
                files=files_table)


TRANSFER_HELP = """
Transfer files from this machine to other echomesh nodes.

transfer file-or-directory [file-or-directory...]:
  Transfers one or more command files or directories to other echomesh nodes.
  Files or directories on the receiving end are removed and replaced by the
  data from this node.

transfer *
  Transfers all command files to all other echomesh nodes.
  Any other command files on other nodes will be deleted and overwritten.

transfer
  Like transfer *, but prompts to make sure that you want to do it.
"""

Register.register('transfer', transfer, TRANSFER_HELP)
