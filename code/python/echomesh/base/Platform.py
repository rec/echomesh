from __future__ import absolute_import, division, print_function, unicode_literals

import platform

PLATFORM = platform.system().lower()

IS_LINUX = (PLATFORM == 'linux')

if IS_LINUX:
  PLATFORM = platform.linux_distribution()[0].lower()

DEBIAN = 'debian'
MAC = 'darwin'
UBUNTU = 'ubuntu'
WINDOWS = 'windows'

LEGAL_PLATFORMS = DEBIAN, MAC, UBUNTU, WINDOWS

assert PLATFORM in LEGAL_PLATFORMS, "Don't understand platform %s" % PLATFORM

