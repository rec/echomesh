from __future__ import absolute_import, division, print_function, unicode_literals

class Openable(object):
  def __init__(self):
    self.is_open = True

  def start(self):
    pass

  def close(self):
    self.is_open = False

  def __enter__(self):
    return self

  def __exit__(self, type, value, traceback):
    self.close()
