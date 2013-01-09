from __future__ import absolute_import, division, print_function, unicode_literals

import functools
import os

from Tkinter import Tk

class Panel(Tk):
  @functools.wraps(Tk.__init__)
  def __init__(self, **kwds):
    display = os.environ.get('DISPLAY', None)
    if not display:
      os.environ['DISPLAY'] = ':0'
    Tk.__init__(self, **kwds)

