#!/usr/bin/python

class Locker(object):
  def __init__(self, lock):
    self.lock = lock

  def __enter__(self):
    self.lock.acquire()

  def __exit__(self, type, value, traceback):
    self.lock.release()
