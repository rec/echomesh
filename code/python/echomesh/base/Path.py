from __future__ import absolute_import, division, print_function, unicode_literals

import os
import os.path
import sys

CODE_PATH = os.path.abspath(sys.path[0])
ECHOMESH_PATH = os.path.dirname(os.path.dirname(CODE_PATH))

def yaml_args():
  return [a for a in sys.argv if _is_yaml(a)]

def _is_yaml(x):
  return x and (x[0] in '{[')

def _not_possible_project(path):
  for d in 'asset', 'command':
    if not os.path.exists(os.path.join(path, d)):
      return True

def _set_project_path():
  arg = (sys.argv + [''])[1]
  if arg == 'autostart':
    arg = ''

  original_path = arg or (os.path.abspath(os.curdir))
  path = os.path.abspath(os.path.expanduser(original_path))

  while _not_possible_project(path):
    p = os.path.dirname(path)
    if p == path:
      print("The path %s wasn't in an echomesh project " % original_path)
      return
    path = p

  return path

PROJECT_PATH = _set_project_path()
COMMAND_PATH = os.path.join(PROJECT_PATH, 'command')
ASSET_PATH = os.path.join(PROJECT_PATH, 'asset')

os.chdir(PROJECT_PATH)


def info():
  return {
    'Asset path': ASSET_PATH,
    'Code path': CODE_PATH,
    'Command path': COMMAND_PATH,
    'Project path': PROJECT_PATH,
    'echomesh path': ECHOMESH_PATH,
    }
