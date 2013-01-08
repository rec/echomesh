from __future__ import absolute_import, division, print_function, unicode_literals

import platform

PLATFORM = platform.system()

IS_LINUX = (PLATFORM == 'Linux')
IS_MAC = (PLATFORM == 'Darwin')
IS_WINDOWS = (PLATFORM == 'Windows')

assert IS_LINUX or IS_MAC or IS_WINDOWS
