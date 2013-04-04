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

THREAD = None

TKWIN = None

class Tkwin(object):
  def __init__(self):
    self.is_running = True
    self.tkwin = Tkinter.Tk()
    self.tkwin.geometry('200x200')
    self.tkwin.update()
    self.is_black = True
    self.thread = threading.Thread(target=self.target)
    self.thread.start()

  def target(self):
    while self.is_running:
      time.sleep(1)
      self.tkwin.configure(background='black' if self.is_black else 'white')
      self.is_black = not self.is_black
      self.tkwin.update()

while RUNNING:
  print('command:', )
  item = sys.stdin.readline().strip().lower()
  print('command was', item)
  if item == 'quit':
    quit()
  elif item == 'hello':
    print('world')
  elif item == 'start':
    if not TKWIN:
      TKWIN = Tkwin()
    else:
      print('already started!')
  elif item == 'stop':
    if TKWIN:
      TKWIN.is_running = False
      TKWIN = None
    else:
      print('not running!')
  else:
    print("Didn't understand", item)



