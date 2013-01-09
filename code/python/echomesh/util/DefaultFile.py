from __future__ import absolute_import, division, print_function, unicode_literals

import os.path
import sys

class DefaultFile(object):
  def __init__(self, directory):
    self.directory = os.path.abspath(directory)

  def expand(self, file):
    if not os.path.isabs(file):
      file = os.path.join(self.directory, file)
    return file

  def relpath(self, file):
    f = os.path.relpath(file, self.directory)
    return file if f.startswith('..') else f
