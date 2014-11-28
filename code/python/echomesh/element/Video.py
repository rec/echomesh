from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.element.Execute import Execute
from echomesh.util import Log
from echomesh.base import Platform

LOGGER = Log.logger(__name__)

ARGS = {
  Platform.RASPBERRY_PI: [],
  Platform.UBUNTU: [
    '--fullscreen',
    '--key-leave-fullscreen',
    '--overlay',
    '--play-and-stop',
    '--video-on-top',
    ],
}

BINARY = {
  Platform.RASPBERRY_PI: '/usr/bin/omxplayer',
  Platform.UBUNTU: '/usr/bin/cvlc',
}

class Video(Execute):
    def __init__(self, parent, desc):
        desc['args'] = desc['args'] or ARGS.get(Platform.PLATFORM)
        desc['binary'] = desc.get('binary') or BINARY.get(Platform.PLATFORM)
        if not desc['binary']:
            raise Exception("Couldn't locate video binary for platform %s",
                            Platform.PLATFORM)

        super(Video, self).__init__(parent, desc)
