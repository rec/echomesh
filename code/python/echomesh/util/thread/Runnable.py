from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Log

LOGGER = Log.logger(__name__)

class Runnable(object):
    """
    A Runnable is a class that be run, paused and begin.  A Runnable must
    implement at least one of _on_run or _on_pause, and most likely _on_begin
    too.
    """
    def __init__(self):
        self.is_running = False
        self.begin_called = False

    def run(self):
        """Continue running from where we were before, if we aren't running now.
        """
        if not self.is_running:
            self.is_running = True
            if not self.begin_called:
                self.begin()

            if self._on_run():
                self.pause()
                LOGGER.vdebug('%s paused in startup', self)
            else:
                LOGGER.vdebug('Started %s', self)
        else:
            LOGGER.vdebug('Tried to run a running %s', self)

    def pause(self):
        """Pause running, if we are running."""
        if self.is_running:
            self.is_running = False
            self._on_pause()
            LOGGER.vdebug('Paused %s', self)
        else:
            LOGGER.vdebug('Tried to pause a paused %s', self)

    def begin(self):
        """Reset this Runnable to the beginning, whether or not it's running."""
        LOGGER.vdebug('Resetting %s', self)
        self.begin_called = True
        self._on_begin()

    def start(self):
        """Start is equivalent to begin() followed by run()."""
        self.begin()
        self.run()

    def unload(self):
        """Unload is called when the runnable is unloaded from memory."""
        pass

    def _on_run(self):
        """This is called on a state change from not running to running.
        This function should return True if the Runnable was either unable to
        run or must pause immediately ("one-shots" like element.Print).
        """
        pass

    def _on_pause(self):
        """This is called on a state change from running to not running."""
        pass

    def _on_begin(self):
        """This is called by begin and by the constructor of Runnable.
        self.is_running might or might not be true.
        """
        pass

    # TODO: can I delete these next two since we aren't using this as a context?
    def __enter__(self):
        return self

    def __exit__(self, _type, value, traceback):
        self.pause()
