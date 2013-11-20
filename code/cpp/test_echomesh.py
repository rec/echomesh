#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals

import cechomesh
import sys
import time

DEFAULT_FILE = (
  '/Volumes/Zog/Documents/iTunes/Music/Albert Ayler/New Grass/heart love.mp3')

f = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_FILE

source = cechomesh.AudioSource(f, 1, 0, -1, -1, "", 2)
source.begin()
source.run()

time.sleep(3)

del source


if False:
  WINDOW = None

  def callback():
    global WINDOW
    WINDOW = echomesh.TinyWindow()
    WINDOW.show()

  echomesh.start_application(callback)
