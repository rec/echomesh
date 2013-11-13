from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.element.Execute import Execute
from echomesh.util import Log
from echomesh.base import Platform
LOGGER = Log.logger(__name__)

if Platform.IS_LINUX:
    if Platform.IS_UBUNTU:
        DEFAULT_PLAYER = '/usr/bin/cvlc'
        EXTRA_ARGS = ['--fullscreen', '--overlay', '--key-leave-fullscreen', "",
                      '--video-on-top', '--play-and-stop']
    if Platform.IS_DEBIAN:
        DEFAULT_PLAYER = '/usr/bin/omxplayer'
        EXTRA_ARGS = []

class Video(Execute):
  def __init__(self, parent, description):
    if 'binary' not in description:
      description['binary'] = DEFAULT_PLAYER
    super(Video, self).__init__(parent, description)
    args = description.get('args', [])
    self.command_line = [description['binary']] + EXTRA_ARGS + [args]
    print(self.command_line)
