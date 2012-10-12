from __future__ import absolute_import, division, print_function, unicode_literals


import ossaudiodev

def print_fmts(rw):
  print(rw == 'r' and 'read' or 'write')
  sound = ossaudiodev.open(rw)
  fmts = sound.getfmts()

  for name in dir(ossaudiodev):
    if name.startswith('AFMT'):
      attr = getattr(ossaudiodev, name)
      if attr & fmts:
        print(name)

  print()
  sound.close()

print_fmts('w')
print_fmts('r')
