from __future__ import absolute_import, division, print_function, unicode_literals

_LEVEL = 0
_ADDED = False

def _level_client(input):
  global _LEVEL
  _LEVEL = input.level

def input_level():
  global _ADDED
  if not _ADDED:
    from echomesh.sound import InputManager
    InputManager.INPUT_MANAGER.add_client(_level_client)
    _ADDED = True
  return _LEVEL
