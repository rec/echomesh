from __future__ import absolute_import, division, print_function, unicode_literals

import time

from echomesh.element import Element
from echomesh.element import Load
from echomesh.element import Loop
from echomesh.util import Log
from echomesh.util.math import Units

LOGGER = Log.logger(__name__)

# TODO: how does a sequence autostop?
class Sequence(Loop.Loop):
  ATTRIBUTES = 'begin', 'end', 'duration'
  BEGIN, END, END_OF_SEQUENCE = range(3)

  def __init__(self, parent, description):
    times = []
    for e in description.elements:
      times.append([Units.convert(e.pop(a)) for a in Sequence.ATTRIBUTES])

    super(Sequence, self).__init__(parent, description, name='Sequence')
    self.loops = Units.convert(description.get('loops', 1))
    self.duration = Units.convert(description.get('duration'), Units.INFINITY)

    self.sequence = []
    for element, t in zip(self.elements, times):
      begin, end, duration = t
      if duration is not None:
        if end is not None:
          begin = end - duration
        elif begin is not None:
          end = begin + duration

      if begin is not None:
        self.sequence.append([begin, element, Sequence.BEGIN])

      if end is not None:
        self.sequence.append([end, element, Sequence.END])

    self.sequence.append([duration, None, Sequence.END_OF_SEQUENCE])
    self.sequence.sort(key=0)

  def _command_time(self):
    return self.sequence[self.next_command][0] + self.start_time

  def next_time(self, t):
    if self.next_command <= len(self.element):
      LOGGER.debug('Running command %d', self.next_command)
      return self._command_time()
    else:
      self.current_loop += 1
      if self.current_loop < self.loops:
        self.start_time = time.time()
        self.next_command = 0
        return self._command_time()
      else:
        LOGGER.info('Sequence finished')
        self.pause()
        return 0

  def _on_reset(self):
    self.current_loop = 0
    self.next_command = 0

  def loop_target(self, t):
    while self.next_command < len(self.sequence) and self._command_time() <= t:
      LOGGER.debug('%d', self.next_command)
      if self.next_command < len(self.elements):
        t, element, cmd = self.sequence[self.next_command]

      self.next_command += 1

Element.register(Sequence)
