from __future__ import absolute_import, division, print_function, unicode_literals

import os

from echomesh.base import Config
from echomesh.util import Log
from echomesh.util import TestSuperuser

LOGGER = Log.logger(__name__)

BLACKLIST_FILE = '/etc/modprobe.d/raspi-blacklist.conf'
BLACKLIST_TEMP = '/tmp/raspi-blacklist.conf'

def _blacklist_line(line):
  return line.strip().startswith('blacklist spi')

def _is_blacklisted():
  try:
    with open(BLACKLIST_FILE, 'rb') as f:
      LOGGER.info('You are running the Raspian distribution, '
                  'blacklist file is here:')
      LOGGER.info(BLACKLIST_FILE)
      return any(_blacklist_line(line) for line in f)
  except:
    LOGGER.warning('You are not running the Raspian distribution, '
                   'no blacklist found.')

def _fix_blacklist():
  try:
    with open(BLACKLIST_FILE, 'rb') as f:
      with open(BLACKLIST_TEMP, 'wb') as g:
        for line in f:
          if _blacklist_line(line):
            line = '#' + line
          g.write(line)
    os.rename(BLACKLIST_TEMP, BLACKLIST_FILE)

  except Exception:
    LOGGER.error("Couldn't fix blacklist.")


_SPEEDUP_ERROR = """
Couldn't speed up SPI, please install py-spidev by typing.

sudo apt-get install -y pyspidev

at the command line.
"""
def _speedup():
  try:
    import spidev
    spi = spidev.SpiDev()
  except:
    LOGGER.error(_SPEEDUP_ERROR)
  else:
    spi.open(0, 0)
    spi.max_speed_hz = 20000000

BLACKLISTED_MESSAGE = """\
SPI has been blacklisted on your machine, which means you won't be able to
control any lights until that is changed.
"""

BLACKLIST_FIXED = """\

The SPI blacklist has been removed.  Please restart your Raspberry Pi
and run echomesh again."""

def _fix_spi(prompt_to_fix):
  if _is_blacklisted():
    LOGGER.info(BLACKLISTED_MESSAGE)
    if prompt_to_fix:
      print('Would you like to fix the blacklist now? (y/N) ', end='')
      result = raw_input()
      if result.lower().startswith('y'):
        _fix_blacklist()
        LOGGER.error()
    LOGGER.error("SPI is blacklisted, lights are disabled.")

SPI_ERROR = """\
you have lights enabled, the lights require SPI, and the SPI driver
needs to be run as root."""

def _test_spi(prompt_to_fix):
  try:
    TestSuperuser.test_superuser(SPI_ERROR)
  except:
    LOGGER.info('')
    LOGGER.error()
  else:
    _speedup()
    return _fix_spi(prompt_to_fix)

_LIGHTS_ENABLED = None

def lights_enabled(prompt_to_fix=False):
  global _LIGHTS_ENABLED
  if _LIGHTS_ENABLED is None:
    _LIGHTS_ENABLED = (Config.get('light', 'enable')
                       and _test_spi(prompt_to_fix)) or False
  return _LIGHTS_ENABLED
