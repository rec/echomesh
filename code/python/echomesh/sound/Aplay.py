from __future__ import absolute_import, division, print_function, unicode_literals

import threading

from echomesh.base import Config
from echomesh.base import Platform
from echomesh.sound import Util
from echomesh.util import Log
from echomesh.util import Subprocess

LOGGER = Log.logger(__name__)

def play(filename, run_in_thread=True):
  filename = Util.DEFAULT_AUDIO_DIRECTORY.expand(filename)
  binary = Config.get('audio', 'output', 'aplay_binary')
  if not binary:
    if Platform.IS_LINUX:
      binary = '/usr/bin/mpg123'
    elif Platform.IS_MAC:
      binary = '/usr/bin/afplay'

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
