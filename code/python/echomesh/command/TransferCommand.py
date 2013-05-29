from __future__ import absolute_import, division, print_function, unicode_literals

import os
import os.path

from echomesh.base import Path
from echomesh.command import CommandRegistry
from echomesh.util import Log

LOGGER = Log.logger(__name__)

TRANSFER_PROMPT =  """
Are you sure you want to transfer all command files over to all echomesh nodes
on this network, replacing whatever is there (y/N)?
"""

TRANSFER_ALL_FILES = True

def transfer(echomesh_instance, *path):
  if not path:
    LOGGER.info(TRANSFER_PROMPT)
    if not raw_input().lower().startswith('y'):
      LOGGER.info('Transfer cancelled.')
      return
    path = ['*']
  if '*' in path or '.' in path:
    path = ['']

  files, directories = _get_files_to_transfer(path)

  s = '' if len(files) is 1 else 's'
  LOGGER.info('Transferred %d file%s.', len(files), s)
  echomesh_instance.send(type='transfer',
                         directories=sorted(directories),
                         files=files)

def _get_files_to_transfer(path):
  files = set()
  directories = set()

  for p in path:
    f = os.path.join(Path.COMMAND_PATH, p)
    if not os.path.exists(f):
      raise Exception("Command file %s doesn't exist.", f)
    walk = os.walk(f)
    if walk:
      directories.add(p)
      for root, _, fs in walk:
        if not root.startswith('.'):
          for ffs in fs:
            if TRANSFER_ALL_FILES or ffs.endswith('.yml'):
              files.add(os.path.join(Path.COMMAND_PATH, root, ffs))
      LOGGER.debug('Adding directory %s', p)
    else:
      LOGGER.debug('Adding file %s', p)
      files.add(f)

  return _get_files_table(files), directories

def _get_files_table(files):
  files_table = {}
  files = sorted(files)
  for f in files:
    stat = os.stat(f)
    contents = None
    try:
      with open(f, 'rb') as fs:
        contents = fs.read()
    except:
      LOGGER.error('Got an unexpected error reading a file %s', f, exc_info=1)
    else:
      files_table[f] = {'contents': contents,
                        'atime': stat.st_atime,
                        'mtime': stat.st_mtime}
  return files_table


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

CommandRegistry.register(transfer, 'transfer', TRANSFER_HELP)
