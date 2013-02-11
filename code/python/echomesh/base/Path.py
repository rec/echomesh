from __future__ import absolute_import, division, print_function, unicode_literals

import os
import os.path
import sys

CODE_PATH = os.path.abspath(sys.path[0])
ECHOMESH_PATH = os.path.dirname(os.path.dirname(CODE_PATH))
PROJECT_PATH = ECHOMESH_PATH

def _not_possible_project(path):
  for d in 'asset', 'command':
    if not os.path.exists(os.path.join(path, d)):
      return True

def set_project_path(original_path=None):
  original_path = original_path or (os.path.abspath(os.curdir))
  path = os.path.abspath(os.path.expanduser(original_path))

  while _not_possible_project(path):
    p = os.path.dirname(path)
    if p == path:
      print("The path %s wasn't in an echomesh project " % original_path)
      return
    path = p

  os.chdir(path)

  global PROJECT_PATH
  PROJECT_PATH = path

