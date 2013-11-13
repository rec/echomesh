from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.element.Execute import Execute
from echomesh.util import Log

LOGGER = Log.logger(__name__)

DEFAULT_PLAYER = '/usr/bin/cvlc'

class Video(Execute):
  def __init__(self, parent, description):
    if 'binary' not in description:
      description['binary'] = DEFAULT_PLAYER
    super(Video, self).__init__(parent, description)
    args = description.get('args', [])
    self.command_line = [description['binary'], '--fullscreen', '--overlay',
                         '--key-leave-fullscreen', "", '--video-on-top', '--play-and-stop', '%s' % args]
    print(self.command_line)

