#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals

import cechomesh
import time

source = cechomesh.AudioSource('/Volumes/Zog/Documents/iTunes/Music/Albert Ayler/New Grass/heart love.mp3', 1, 0, -1, -1, "", 2)
source.begin()
source.run()

time.sleep(10)

del source


if False:
  WINDOW = None

  def callback():
    global WINDOW
    WINDOW = echomesh.TinyWindow()
    WINDOW.show()

  echomesh.start_application(callback)
