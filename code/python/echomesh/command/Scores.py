from __future__ import absolute_import, division, print_function, unicode_literals

import os
import os.path
import time

from echomesh.base import Path
from echomesh.base import DataFileName
from echomesh.util import Log
from echomesh.util import Context
from echomesh.util.string import Flag
from echomesh.util.string import SizeName

LOGGER = Log.logger(__name__)

ONE_DAY = 60 * 60 * 24

def _time(t):
  if (time.time() - t) >= ONE_DAY:
    fmt = '%d %b'
  else:
    fmt = ' %H:%M'
  return time.strftime(fmt, time.localtime(t))

#                 file   bytes a   m   c
ELEMENT_FORMAT = '  %-28s %5s %9s %9s %9s'
INDENT = '  '

def _scores(path, resolve=False, context='all', recursive=False,
            indent='', printed=False, top_level=True):
  if context == 'all':
    for c in Context.CONTEXTS:
      printed = _scores(path, resolve, c, recursive, indent) or printed
  else:
    context = Context.resolve(context)
    pathdir = os.path.join(Path.data_path(), context, 'score', path)
    if os.path.isdir(pathdir):
      printed_this_time = False
      for f in sorted(os.listdir(pathdir)):
        joined_f = os.path.join(pathdir, f)
        is_dir = os.path.isdir(joined_f)
        if not (is_dir or DataFileName.has_extension(f)):
          continue
        if not printed_this_time:
          printed_this_time = True
          if not printed:
            LOGGER.info(indent + ELEMENT_FORMAT, 'File name', ' Bytes', 'Accessed',
                         'Modified', 'Created')
            printed = True
          elif top_level:
            LOGGER.info('\n')
          if top_level:
            LOGGER.info('    %s/%s:', context, path)
        if is_dir:
          if recursive:
            LOGGER.info('')
          LOGGER.info('      %s/', f)
          if recursive:
            _scores(os.path.join(path, f), resolve, context, recursive,
                    indent + INDENT, printed=True, top_level=False)
            LOGGER.info('')

        else:
          stat = os.stat(joined_f)
          LOGGER.info(indent + ELEMENT_FORMAT,
                       '    ' + f, SizeName.size_name(stat.st_size),
                       _time(stat.st_atime),
                       _time(stat.st_mtime),
                       _time(stat.st_ctime))
  return printed

SCORES_HELP = """
"show scores" shows some or all of the scores in the echomesh project.

Because of the resolution of score names, there are multiple areas where scores
might be found, called "contexts".

If you just type "show scores" you'll see all in the top directory.
If you want to see items in a subdirecto

The full form of the command is

  show scores

See "help show contexts" for more information.
"""

def scores(_, *args):
  flags, paths = Flag.split_flag_args(args)
  paths = paths or ['']
  printed = False
  for p in paths:
    printed = _scores(p, **flags) or printed

  if printed:
    LOGGER.info('')
  else:
    LOGGER.info('  No matching scores found.\n')
