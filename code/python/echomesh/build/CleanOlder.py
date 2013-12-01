from __future__ import absolute_import, division, print_function, unicode_literals

import os

from echomesh.build.BuildConfig import CONFIG

def _is_newer(f1, f2):
  return os.stat(f1).st_mtime > os.stat(f2).st_mtime

def clean_older():
  if _is_newer(CONFIG.c_library, CONFIG.library_name):
    os.remove(CONFIG.library_name)
    if CONFIG.verbose:
      print('Removed old library %s.' % CONFIG.library_name)
