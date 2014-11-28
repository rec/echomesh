from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Platform

_MAC_BUILD = ('xcodebuild -project Builds/MacOSX/echomesh.xcodeproj '
                 '-configuration {Config} ')

_RASPBERRY_PI_BUILD = ('cd Builds/Linux && make -k ')

COMMANDS = {
  'library': {
    Platform.MAC: _MAC_BUILD,
    Platform.RASPBERRY_PI: _RASPBERRY_PI_BUILD
  },
  'clean': {
    Platform.MAC: _MAC_BUILD + 'clean',
    Platform.RASPBERRY_PI: _RASPBERRY_PI_BUILD + 'clean'
  },
}
