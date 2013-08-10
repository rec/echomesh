def _fix_path():
  import os
  import sys

  cwd = os.getcwd()

  for c in cwd, os.path.join(cwd, 'external'):
    if c not in sys.path:
      sys.path.insert(0, c)

# _fix_path()
