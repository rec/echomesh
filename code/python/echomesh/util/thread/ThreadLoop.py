from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util.thread.ThreadRunnable import ThreadRunnable

class ThreadLoop(ThreadRunnable):
  def __init__(self, single_loop=None, name=None, report_error=False,
               is_daemon=True):
    super(ThreadLoop, self).__init__(report_error=report_error,
                                     is_daemon=is_daemon)
    self.name = name or repr(self)
    self._single_loop = single_loop or self.single_loop
    assert self._single_loop

  def single_loop(self):
    pass

  def target(self):
    while self.is_running:
      self._single_loop()
