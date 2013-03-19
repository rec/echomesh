from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Log

LOGGER = Log.logger(__name__)

class Runnable(object):
  """
  A Runnable is a class that be run, paused and reset.  A Runnable must
  implement at least one of _on_run or _on_pause, and most likely _on_reset too.
  """
  def __init__(self):
    self.is_running = False
    self.reset_called = False

  def run(self):
    """Continue running from where we were before, if we aren't running now."""
    if not self.is_running:
      self.is_running = True
      if not self.reset_called:
        self.reset()

      if self._on_run():
        self.pause()
        LOGGER.debug('%s paused in startup', self)
      else:
        LOGGER.debug('Started %s', self)
    else:
      LOGGER.debug('Tried to run a running %s', self)

  def pause(self):
    """Pause running, if we are running."""
    if self.is_running:
      self.is_running = False
      self._on_pause()
      LOGGER.debug('Paused %s', self)
    else:
      LOGGER.debug('Tried to pause a paused %s', self)

  def reset(self):
    """Reset this Runnable to the beginning, whether or not it is running."""
    LOGGER.debug('Resetting %s', self)
    self.reset_called = True
    self._on_reset()

  def start(self):
    """Start is equivalent to reset() followed by run()."""
    self.reset()
    self.run()

  def _on_run(self):
    """This is called on a state change from not running to running.
    This function should return True if the Runnable was either unable to run
    or must pause immediately ("one-shots" like element.Print).
    """
    pass

  def _on_pause(self):
    """This is called on a state change from running to not running."""
    pass

  def _on_reset(self):
    """This is called by reset and by the constructor of Runnable.
    self.is_running might or might not be true.
    """
    pass

  # TODO: can I delete these next two since we aren't using this as a context?
  def __enter__(self):
    return self

  def __exit__(self, _type, value, traceback):
    self.pause()
