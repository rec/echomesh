from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Log

LOGGER = Log.logger(__name__)

class Runnable(object):
  """
  A Runnable is a class that be run, stopped and reset.  A Runnable must
  implement at least one of _on_run or _on_stop, and most likely _on_reset too.
  """
  def __init__(self):
    self.is_running = False
    self._on_reset()

  def run(self):
    """Continue running from where we were before, if we aren't running now."""
    if not self.is_running:
      self.is_running = True
      if self._on_run():
        self.stop()
        LOGGER.debug('%s stopped in startup', self)
      else:
        LOGGER.debug('Started %s', self)
    else:
      LOGGER.debug('Tried to run a running %s', self)

  def stop(self):
    """Stop running, if we are running."""
    if self.is_running:
      self.is_running = False
      self._on_stop()
      LOGGER.debug('Stopped %s', self)
    else:
      LOGGER.debug('Tried to stop a stopped %s', self)

  def reset(self):
    """Reset this Runnable to the beginning, whether or not it is running."""
    LOGGER.debug('Resetting %s', self)
    self._on_reset()

  def start(self):
    """Start is equivalent to reset() followed by run()."""
    self.reset()
    if not self.running:
      self.run()

  def _on_run(self):
    """This is called on a state change from not running to running.
    This function should return True if the Runnable was either unable to run
    or must stop immediately ("one-shots" like element.Print).
    """
    pass

  def _on_stop(self):
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

  def __exit__(self, type, value, traceback):
    self.stop()
