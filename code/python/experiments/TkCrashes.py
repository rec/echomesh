#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import threading
import time

import Queue
import Tkinter

QUEUE = Queue.Queue()
TIMEOUT = 2
BLOCKING = (TIMEOUT is not None)
USE_STDIO = False

RUNNING = True

def read_keyboard():
  time.sleep(1)
  global RUNNING
  while RUNNING:
    print('reading keyboard...')
    if USE_STDIO:
      item = sys.stdin.readline()
    else:
      item = raw_input()  # The program crashes almost immediately after this returns.
    item = item.strip().lower()
    print('read_keyboard:', item)
    if item == 'quit':
      RUNNING = False
    else:
      QUEUE.put(item)

THREAD = threading.Thread(target=read_keyboard)
THREAD.start()

print('starting loop')
INDEX = 1
while RUNNING:
  try:
    print(INDEX)
    INDEX += 1
    item = QUEUE.get(BLOCKING, TIMEOUT)
  except Queue.Empty:
    continue
  else:
    if item == 'tk':
      tkwin = Tkinter.Tk()
      tkwin.geometry('200x200')
      tkwin.update()
    elif item == 'hello':
      print('world')
    else:
      print("Don't understand", item)

