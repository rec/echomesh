from __future__ import absolute_import, division, print_function, unicode_literals

import cechomesh

def scroll(colors, dx, dy, x_size, smooth=True, wrap=False):
  bx, by = int(dx), int(dy)
  if (not smooth) or (bx == dx and by == dy):
    return cechomesh.scroll_color_list(colors, dx, dy, x_size, wrap)
