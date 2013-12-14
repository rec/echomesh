from __future__ import absolute_import, division, print_function, unicode_literals

import operator
import time

from echomesh.element import Loop
from echomesh.expression import Expression
from echomesh.expression import UnitConfig
from echomesh.pattern import PatternDesc
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class Sequence(Loop.Loop):
  ATTRIBUTES = 'begin', 'end', 'duration'

  def __init__(self, parent, desc):
    times = []
    for e in desc.get('elements', []):
      times.append([Expression.convert(e.pop(a, None)) for a in Sequence.ATTRIBUTES])

    self.elements = []
    self.pattern_makers = PatternDesc.make_patterns_for_element(
      self, desc.get('patterns', {}))
    super(Sequence, self).__init__(
      parent, desc, name='Sequence', full_slave=False)
    self.loops = Expression.convert(desc.get('loops', 1))
    self.duration = Expression.convert(desc.get('duration', 'infinity'))
    self.sequence = []
    self.paused_children = set()

    for element, t in zip(self.elements, times):
      begin, end, duration = t
      if duration is not None:
        if end is not None:
          begin = end - duration
        elif begin is not None:
          end = begin + duration

      self.sequence.append([begin or 0, element.start])

      if end is not None:
        self.sequence.append([end, element.pause])

    self.sequence.append([self.duration, self.pause])
    self.sequence.sort(key=operator.itemgetter(0))

  def _command_time(self):
    return (self.sequence[self.next_command][0] / UnitConfig.get('speed') +
            self.cycle_time)

  def next_time(self, t):
    if self.next_command <= len(self.elements):
      return self._command_time()
    else:
      self.current_loop += 1
      if self.current_loop < self.loops:
        self.cycle_time = time.time()
        self.next_command = 0
        return self._command_time()
      else:
        self.pause()
        return 0

  def _on_begin(self):
    super(Sequence, self)._on_begin()
    self.cycle_time = self.start_time
    self.current_loop = 0
    self.next_command = 0

  def _on_run(self):
    super(Sequence, self)._on_run()
    self.cycle_time = self.start_time

  def loop_target(self, t):
    while self._command_time() <= t:
      if self.next_command >= len(self.sequence):
        self.pause()
        break
      self.sequence[self.next_command][1]()
      self.next_command += 1

  def child_paused(self, child):
    self.paused_children.add(child)
    if self.paused_children == set(self.elements):
      self.pause()
