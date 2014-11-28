from __future__ import absolute_import, division, print_function, unicode_literals

import platform

PLATFORM = platform.system().lower()

DEBIAN = 'debian'
MAC = 'darwin'
RASPBERRY_PI = 'raspberry-pi'
UBUNTU = 'ubuntu'
WINDOWS = 'windows'

IS_LINUX = (PLATFORM == 'linux')

if IS_LINUX:
    PLATFORM = platform.linux_distribution()[0].lower()
    if PLATFORM == DEBIAN:
        try:
            with open('/proc/cpuinfo') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('Hardware') and line.endswith('BCM2708'):
                        PLATFORM = RASPBERRY_PI
                        break
        except:
            pass

LEGAL_PLATFORMS = DEBIAN, MAC, RASPBERRY_PI, UBUNTU, WINDOWS

assert PLATFORM in LEGAL_PLATFORMS, "Don't understand platform %s" % PLATFORM
