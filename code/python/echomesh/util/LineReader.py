from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Yaml

class LineReader(object):
  def __init__(self, callback):
    self.lines = []
    self.results = []
    self.callback = callback

  def add(self, line):
    if line:
      if line.startswith(Yaml.SEPARATOR_BASE):
        if self.callback and self.lines:
          res = ''.join(self.lines)
          result = Yaml.decode_one(res)
          self.callback(result)
        self.lines = []
      else:
        self.lines.append(line)

