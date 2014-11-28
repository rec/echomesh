from __future__ import absolute_import, division, print_function, unicode_literals

import subprocess

from echomesh.util import Log

LOGGER = Log.logger(__name__)

def run(command, **kwds):
    popen = subprocess.Popen(command, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, **kwds)
    popen.wait()
    result = popen.stdout.read().splitlines()
    if popen.returncode:
        LOGGER.error('Command failed with returncode %d', popen.returncode)

    return result, popen.returncode
