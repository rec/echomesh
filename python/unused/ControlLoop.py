from __future__ import absolute_import, division, print_function, unicode_literals

import pygame
import time

from util import Openable
from util import ThreadLoop

class ControlLoop(ThreadLoop.ThreadLoop):
  def __init__(self, config, clock):
    ThreadLoop.ThreadLoop.__init__(self)
    self.config = config
    self.clock = clock
    self.tasks = []

  def run(self):
    now = time.time()
    tasks = []
    for task in self.tasks:
      if task.is_open:
        task.update(now)
        tasks.append(task)

    self.tasks = tasks
    pygame.display.flip()
    self.clock.tick(self.config['frames_per_second'])

# TODO: needs locking.

