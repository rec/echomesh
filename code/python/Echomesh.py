#!/usr/bin/env python2.7

if __name__ == '__main__':
  from echomesh.base import Version

  if Version.TOO_OLD:
    from echomesh.util import TooOld
    TooOld.too_old()
    exit(-1)

  from echomesh import Main
  Main.main()
