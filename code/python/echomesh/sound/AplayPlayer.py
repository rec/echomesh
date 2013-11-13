from __future__ import absolute_import, division, print_function, unicode_literals

# Obsolete, given we're playing in C++.

import threading

from echomesh.base import Config
from echomesh.base import Platform
from echomesh.sound import Util
from echomesh.util import Log
from echomesh.util import Subprocess

LOGGER = Log.logger(__name__)

BINARY = {
  Platform.DEBIAN: '/usr/bin/mpg123',
  Platform.MAC: '/usr/bin/afplay',
  Platform.UBUNTU: '/usr/bin/mpg123',
}

def play(filename, run_in_thread=True):
  filename = Util.DEFAULT_AUDIO_DIRECTORY.expand(filename)
  binary = (Config.get('audio', 'output', 'aplay_binary') or
            BINARY.get(Platform.PLATFORM))

  if not binary:
    LOGGER.error("Couldn't locate binary for platform %s", Platform.PLATFORM)
    return

  def _play():
    _, returncode = Subprocess.run([binary, filename])
    if returncode:
      LOGGER.error('Unable to play file %s using aplay', filename)

  if run_in_thread:
    threading.Thread(target=_play).start()

  else:
    pass  # TODO: Log or something?

def AplayPlayer(_, filename, **kwds):
  return play(filename, **kwds)
