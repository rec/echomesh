from __future__ import absolute_import, division, print_function, unicode_literals

import threading

from echomesh.base import Config
from echomesh.base import Platform
from echomesh.util import Log
from echomesh.util import Subprocess
from echomesh.util.file import DefaultFile

LOGGER = Log.logger(__name__)

DEFAULT_AUDIO_DIRECTORY = DefaultFile.DefaultFile('asset/audio')

def play(file, run_in_thread=True):
  file = DEFAULT_AUDIO_DIRECTORY.expand(file)
  binary = Config.get('audio', 'output', 'aplay_binary')
  if not binary:
    if Platform.IS_LINUX:
      binary = '/usr/bin/mpg123'
    elif Platform.IS_MAC:
      binary = '/usr/bin/afplay'

  if not binary:
    LOGGER.error("Couldn't locate binary for platform %s", Platform.PLATFORM)
    return

  def play():
    result, returncode = Subprocess.run([binary, file])
    if returncode:
      LOGGER.error('Unable to play file %s using aplay', file)

  if run_in_thread:
    threading.Thread(target=play).start()

  else:
    player
