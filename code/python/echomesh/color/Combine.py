from __future__ import absolute_import, division, print_function, unicode_literals

import cechomesh


def combine(*args, **kwds):
  # print('!!!! combine !!!!')
  ret = cechomesh.combine_color_lists(*args, **kwds)
  # print('!!!! combine DONE')
  return ret
