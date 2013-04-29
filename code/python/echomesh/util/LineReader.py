from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Yaml

class LineReader(object):
  def __init__(self):
    self.lines = []
    self.results = []

  def add_line(self, line):
    if line.startswith(Yaml.SEPARATOR_BASE):
      self.lines, lines = [], self.lines
      return Yaml.decode_one(''.join(lines))

    self.lines.append(line)

