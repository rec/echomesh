#!/usr/bin/python

import platform

SYSTEM = platform.system()
IS_LINUX = (SYSTEM == 'Linux')
IS_MAC = (SYSTEM == 'Darwin')
