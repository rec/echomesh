#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals

import cechomesh
import os.path
import sys
import time

ECHOMESH_PYTHON = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'python')

sys.path.insert(1, os.path.join(ECHOMESH_PYTHON, 'external'))
sys.path.insert(1, ECHOMESH_PYTHON)

print(sys.path)


from echomesh.expression.Envelope import Envelope

cechomesh.init_log()

DEFAULT_FILE = (
  '/Volumes/Zog/Documents/iTunes/Music/Albert Ayler/New Grass/heart love.mp3')

f = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_FILE

gain = Envelope({0: 1.0, 2: 0, 4: 1})

source = cechomesh.AudioSource(f, 1, 0, -1, -1, "", 2, None, None)
source.begin()
source.run()

time.sleep(3)

if False:
  WINDOW = None

  def callback():
    global WINDOW
    WINDOW = echomesh.TinyWindow()
    WINDOW.show()

  echomesh.start_application(callback)
