from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.element.Execute import Execute
from echomesh.util import Log
from echomesh.base.Platform import *

LOGGER = Log.logger(__name__)

if IS_LINUX:
    DEFAULT_PLAYER = '/usr/bin/cvlc'
else:
    #Raspberry Pi
    DEFAULT_PLAYER = '/usr/bin/omxplayer'

class Video(Execute):
  def __init__(self, parent, description):
    if 'binary' not in description:
      description['binary'] = DEFAULT_PLAYER
    super(Video, self).__init__(parent, description)

    if IS_LINUX:
        args = description.get('args', [])
        self.command_line = [description['binary'], '--fullscreen', '--overlay',
                             '--key-leave-fullscreen', "", '--video-on-top', '--play-and-stop', '%s' % args]

    else:
        args = description.get('args', [])
        self.command_line = [description['binary'], '%s' % args]

