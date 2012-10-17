from __future__ import absolute_import, division, print_function, unicode_literals

import pygame
import time

from util import Openable
from util import ThreadLoop

class ControlLoop(ThreadLoop.ThreadLoop):
  def __init__(self, config):
    ThreadLoop.ThreadLoop.__init__(self)
    self.config = config
    self.tasks = []

  def runnable(self):
    now = time.time()
    tasks = []
    for task in self.tasks:
      if task.is_open:
        task.update(now)
        tasks.append(task)

    self.tasks = tasks
    pygame.display.flip()
    time.sleep(1.0 / self.config['control_frequency'])

# TODO: needs locking.

