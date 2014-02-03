from __future__ import absolute_import, division, print_function, unicode_literals

_DARWIN_BUILD = ('xcodebuild -project Builds/MacOSX/echomesh.xcodeproj '
                 '-configuration {Config} ')

_DEBIAN_BUILD = ('cd Builds/Linux && make -k ')

COMMANDS = {
  'library': {
    'darwin': _DARWIN_BUILD,
    'debian': _DEBIAN_BUILD
  },
  'clean': {
    'darwin': _DARWIN_BUILD + 'clean',
    'debian': _DEBIAN_BUILD + 'clean'
  },
}

