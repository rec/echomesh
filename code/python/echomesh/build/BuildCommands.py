from __future__ import absolute_import, division, print_function, unicode_literals

_DARWIN_BUILD = ('xcodebuild -project Builds/MacOSX/echomesh.xcodeproj '
                 '-configuration {Config} ')

COMMANDS = {
  'build': {
    'darwin': _DARWIN_BUILD
  },
  'clean': {
    'darwin': _DARWIN_BUILD + 'clean'
  },
}

