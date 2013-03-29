from __future__ import absolute_import, division, print_function, unicode_literals

import operator
import time

from echomesh.element import Element
from echomesh.element import Load
from echomesh.element import Loop
from echomesh.expression import Units
from echomesh.util import Log

LOGGER = Log.logger(__name__)

# TODO: how does a sequence autostop?
class Sequence(Loop.Loop):
  ATTRIBUTES = 'begin', 'end', 'duration'
  def __init__(self, parent, description):
    times = []
    for e in description.get('elements', []):
      times.append([Units.convert(e.pop(a, None)) for a in Sequence.ATTRIBUTES])

    super(Sequence, self).__init__(parent, description, name='Sequence',
                                   full_slave=False)
    self.loops = Units.get_table(description, 'loops', 1)
    self.duration = Units.get_table(description, 'duration', Units.INFINITY)
    self.sequence = []
    self.paused_children = set()

    for element, t in zip(self.elements, times):
      begin, end, duration = t
      if duration is not None:
        if end is not None:
          begin = end - duration
        elif begin is not None:
          end = begin + duration

      if begin is not None:
        self.sequence.append([begin, element.start])

      if end is not None:
        self.sequence.append([end, element.pause])

    self.sequence.append([self.duration, self.pause])
    self.sequence.sort(key=operator.itemgetter(0))

  def _command_time(self):
    return self.sequence[self.next_command][0] + self.cycle_time

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
        LOGGER.info('Sequence finished')
        self.pause()
        return 0

  def _on_reset(self):
    super(Sequence, self)._on_reset()
    self.cycle_time = self.start_time
    self.current_loop = 0
    self.next_command = 0

  def _on_run(self):
    super(Sequence, self)._on_run()
    self.cycle_time = self.start_time

  def loop_target(self, t):
    while self._command_time() <= t:
      LOGGER.debug('%d', self.next_command)
      if self.next_command >= len(self.sequence):
        self.pause()
        break
      self.sequence[self.next_command][1]()
      self.next_command += 1

  def child_paused(self, child):
    self.paused_children.add(child)
    if self.paused_children == set(self.elements):
      self.pause()

Element.register(Sequence)
