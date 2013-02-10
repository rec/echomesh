from __future__ import absolute_import, division, print_function, unicode_literals

import os.path
import sys

class DefaultFile(object):
  def __init__(self, directory):
    self.directory = os.path.abspath(directory)

  def expand(self, f):
    if not os.path.isabs(f):
      f = os.path.join(self.directory, f)
    return f

  def relpath(self, f):
    rel_f = os.path.relpath(f, self.directory)
    return f if rel_f.startswith('..') else rel_f
