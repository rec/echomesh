from __future__ import absolute_import, division, print_function, unicode_literals

import platform

PLATFORM = platform.system().lower()

IS_LINUX = (PLATFORM == 'linux')
IS_MAC = (PLATFORM == 'darwin')
IS_WINDOWS = (PLATFORM == 'windows')

assert IS_LINUX or IS_MAC or IS_WINDOWS

if IS_LINUX:
    DISTRIBUTION = platform.linux_distribution()[0].lower()
    IS_UBUNTU = (DISTRIBUTION == 'ubuntu')
    IS_DEBIAN = (DISTRIBUTION == 'debian')
