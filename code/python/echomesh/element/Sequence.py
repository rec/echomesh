from __future__ import absolute_import, division, print_function, unicode_literals

import time

from echomesh.element import Element
from echomesh.element import Load
from echomesh.element import Loop
from echomesh.util import Log
from echomesh.util.math import Units

LOGGER = Log.logger(__name__)

class Sequence(Loop.Loop):
  def __init__(self, parent, description):
    super(Sequence, self).__init__(parent, description, name='Sequence')
    duration = description.get('duration')
    self.duration = duration and Units.convert(duration)
    self.loops = Units.convert(description.get('loops', 1))
    elements = description.get('elements', [])

    items = ((Units.convert(e.get('begin', 0)),
              Load.make_one(self, e.get('element', {}))) for e in elements)

    self.times, self.elements = zip(*items)
    self.times = list(self.times) + [self.duration]

  def _command_time(self):
    return self.times[self.next_command] + self.start_time

  def next_time(self, t):
    if self.next_command <= len(self.elements):
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
        self.stop()
        return 0

  def _on_start(self):
    self.start_time = time.time()
    self.current_loop = 0
    self.next_command = 0

  def loop_target(self, t):
    while self.next_command <= len(self.elements) and self._command_time() <= t:
      LOGGER.debug('%d', self.next_command)
      if self.next_command < len(self.elements):
        self.elements[self.next_command].start()
      self.next_command += 1

Element.register(Sequence)
