#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals

if __name__ == '__main__':
  try:
    from echomesh import Main
    Main.main()
  except:
    import traceback
    print(traceback.format_exc())
