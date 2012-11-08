from __future__ import absolute_import, division, print_function, unicode_literals

import os.path

class DefaultFile(object):
  def __init__(self, directory='~'):
    self.directory = os.path.expanduser(directory)

  def expand(self, file):
    file = os.path.expanduser(file)
    if not os.path.isabs(file):
      file = os.path.join(self.directory, file)
    return file
