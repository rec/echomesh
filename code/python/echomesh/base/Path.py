from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import MakeEmptyProject
from echomesh.base import Platform

import getpass
import os
import os.path
import sys

# If ECHOMESH_EXTERNALS_OVERRIDE_SYSTEM_PACKAGES is True, you want Echomesh to
# use its own external packages in preference to any you might have installed in
# your system path.
ECHOMESH_EXTERNALS_OVERRIDE_SYSTEM_PACKAGES = True

_PYTHON_PATH = os.path.abspath(sys.path[0])
ECHOMESH_PATH = os.path.dirname(os.path.dirname(_PYTHON_PATH))

_ASSET_PATH = None
_DATA_PATH = None
_PROJECT_PATH = None

_PLATFORM_CPP_PATHS = {
  'ubuntu': 'Builds/Linux/build'
}

_EXTERNAL_CODE_PATH = os.path.join(_PYTHON_PATH, 'external')
_PLATFORM_EXTERNAL_CODE_PATH = os.path.join(
  _EXTERNAL_CODE_PATH, 'platform', Platform.PLATFORM)
LIBRARY_PATH = os.path.join(ECHOMESH_PATH, 'lib', Platform.PLATFORM)
_CPP_BUILD_PATH = os.path.join(
  ECHOMESH_PATH, 'code', 'cpp',
  _PLATFORM_CPP_PATHS.get(Platform.PLATFORM, '')
)
_COMPATIBILITY_PATH = os.path.join(_PYTHON_PATH, 'compatibility')

PATHS = (_CPP_BUILD_PATH, _PLATFORM_EXTERNAL_CODE_PATH, _EXTERNAL_CODE_PATH,
         LIBRARY_PATH, _COMPATIBILITY_PATH)

_REQUIRED_DIRECTORIES = 'asset', 'cache', 'data', 'log'

def data_path():
    _set_project_path()
    return _DATA_PATH

def echomesh_path():
    _set_project_path()
    return ECHOMESH_PATH

def project_path():
    _set_project_path()
    return _PROJECT_PATH

def python_path():
    _set_project_path()
    return _PYTHON_PATH

def _possible_project(path):
    for d in _REQUIRED_DIRECTORIES:
        if not os.path.exists(os.path.join(path, d)):
            return False
    return True

def set_project_path(project_path=None, show_error=True, prompt=True):
    original_path = os.path.abspath(
        os.path.expanduser(project_path or os.curdir))
    path = original_path

    global _PROJECT_PATH, _DATA_PATH, _ASSET_PATH
    while not _possible_project(path):
        p = os.path.dirname(path)
        if p != path:
            path = p
            continue
        if prompt:
            if MakeEmptyProject.ask_to_make_empty_project(original_path):
                path = original_path
                break
            else:
                _PROJECT_PATH = None
                return False
        if show_error:
            print(
                "\nYour path %s isn't in an echomesh project." % original_path)
            print("Defaulting to the echomesh path %s." % ECHOMESH_PATH)
        path = ECHOMESH_PATH
        break

    _PROJECT_PATH = path
    _DATA_PATH = os.path.join(path, 'data')
    _ASSET_PATH = os.path.join(path, 'asset')
    os.chdir(path)
    return True

def _set_project_path():
    if not _PROJECT_PATH:
        set_project_path()

def info():
    _set_project_path()
    return {
      'Asset path': _ASSET_PATH,
      'Code path': _PYTHON_PATH,
      'Compatibility path': _COMPATIBILITY_PATH,
      'C++ build path': _CPP_BUILD_PATH,
      'Data path': _DATA_PATH,
      'External code path': _EXTERNAL_CODE_PATH,
      'Platform external code path': _PLATFORM_EXTERNAL_CODE_PATH,
      'Project path': _PROJECT_PATH,
      'Python path': ':'.join(PATHS),
      'echomesh path': ECHOMESH_PATH,
      }

def fix_sys_path():
    _set_project_path()
    for path in reversed(PATHS):
        if ECHOMESH_EXTERNALS_OVERRIDE_SYSTEM_PACKAGES:
            sys.path.insert(1, path)
        else:
            sys.path.append(path)

_HOME_VARIABLE_FIXED = False

# HACK!
def fix_home_directory_environment_variable():
    if Platform.PLATFORM == Platform.RASPBERRY_PI:
        global _HOME_VARIABLE_FIXED
        if not _HOME_VARIABLE_FIXED:
            # If running as root, export user pi's home directory as $HOME.
            if getpass.getuser() == 'root':
                os.environ['HOME'] = '/home/pi'
            _HOME_VARIABLE_FIXED = True


def fix_paths():
    _set_project_path()
    fix_home_directory_environment_variable()
    fix_sys_path()
