from __future__ import absolute_import, division, print_function, unicode_literals

import os
import os.path
import time

from echomesh.util import Flag
from echomesh.util import Log
from echomesh.util import Scope

LOGGER = Log.logger(__name__)

def _time(t):
  return time.strftime('%H:%M', time.localtime(t))

ELEMENT_FORMAT = '%-28s %5s %9s %9s %9s'

def _elements(path, resolve=False, scope='all', recursive=False):
  printed = False
  if scope == 'all':
    for s in Scope.SCOPES:
      printed = _elements(path, resolve, s, recursive) or printed
  else:
    scope = Scope.resolve(scope)
    pathdir = os.path.join(Path.COMMAND_PATH, scope, 'element', path)
    if os.path.isdir(pathdir):
      printed_this_time = False
      for f in sorted(os.listdir(pathdir)):
        joined_f = os.path.join(pathdir, f)
        is_dir = os.path.isdir(joined_f)
        if not (is_dir or f.endswith('yml')):
          continue
        if not printed_this_time:
          printed_this_time = True
          if not printed:
            LOGGER.print(ELEMENT_FORMAT, 'File name', 'Size', 'Accessed',
                         'Modified', 'Created')
            printed = True
          else:
            LOGGER.print('\n')
          LOGGER.print('  %s/%s:', scope, path)
        if is_dir:
          LOGGER.print('    %s/', f)
        else:
          stat = os.stat(joined_f)
          LOGGER.print(ELEMENT_FORMAT,
                       '    ' + f, SizeName.size_name(stat.st_size),
                       _time(stat.st_atime),
                       _time(stat.st_mtime),
                       _time(stat.st_ctime))
  return printed


ELEMENTS_HELP = """
Shows all the elements in all contexts
"""
def elements(echomesh, *args):
  flags, paths = Flag.split_args(args)
  paths = paths or ['']
  for p in paths:
    _elements(p, **flags)

