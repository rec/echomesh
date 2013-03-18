#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys
import time

BLACKLIST_FILE = '/etc/modprobe.d/raspi-blacklist.conf'
BLACKLIST_TEMP = BLACKLIST_TEMP + '.tmp'

PERM_ERROR = """
This script needs to be run as superuser (because it writes to the SPI driver).
Please rerun it as follows:

  %s
"""

FIX_BLACKLIST_PROMPT = """
The SPI service has been blacklisted on your distribution.

Would you like to fix it now?  You'll need to restart your Raspberry Pi
for the changes to take effect.
"""

DEFAULT_LIGHT_COUNT = 128
DEFAULT_REPEAT_COUNT = 10

LIGHT_COUNT = DEFAULT_LIGHT_COUNT if len(sys.argv) == 1 else int(sys.argv[1])
REPEAT_COUNT = DEFAULT_REPEAT_COUNT if len(sys.argv) < 3 else int(sys.argv[2])

LATCH_BYTE_COUNT = 2
PERIOD = 0.5

def _test_su()
  if os.geteuid():
    raise Exception(PERM_ERROR % ' '.join(['su'] + sys.argv))

def _blacklist_line(line):
  return line.strip().startswith('blacklist spi')

def _is_blacklisted():
  try:
    with open(BLACKLIST_FILE, 'rb') as f:
      print('You are running the Raspian distribution, blacklist file is here:')
      print(' ', BLACKLIST_FILE)
      return any(_blacklist_line(line) for line in f)
  except:
    print('You are not running the Raspian distribution, no blacklist found.')
    pass

def _fix_blacklist():
  try:
    with open(BLACKLIST_FILE, 'rb') as f:
      with open(BLACKLIST_TEMP, 'wb') as g:
        for line in f:
          if _blacklist_line(line):
            line = '#' + line
          g.write(line)
    os.rename(BLACKLIST_TEMP, BLACKLIST_FILE)

  except Exception as e:
    print("Couldn't fix blacklist because error:", e)

def _blacklist():
  if _is_blacklisted():
    print(FIX_BLACKLIST_PROMPT)
    result = raw_input('Fix now? (y/N)')
    if result.lower().startswith('y'):
      _fix_blacklist()
      print('Your blacklist has been fixed.  Please restart your Raspberry Pi\n'
            'and run this program again!')
      return True
    else:
      raise Exception("SPI is blacklisted, can't run lights on your machine.")

def _get_off_on():
  off = bytearray(3 * LIGHT_COUNT + LATCH_BYTE_COUNT)
  on = bytearray(3 * LIGHT_COUNT + LATCH_BYTE_COUNT)

  for i in range(3 * LIGHT_COUNT):
    off[i] = 0x80
    on[i] = 0xFF
  return off, on

def _flash_lights():
  off, on = _get_off_on()
  with open('/dev/spidev0.0', 'wb') as device:
    def write(data, name):
      device.write(data)
      device.flush()
      print(name)
      time.sleep(PERIOD)

    for i in range(REPEAT_COUNT):
      write(on, 'ON!')
      write(off, 'off')

def test_lights():
  try:
    _test_su()
    if not _blacklist():
      _flash_lights()
  except Exception as e:
    print('ERROR:', e)
    exit(-1)


if __name__ == '__main__':
  test_lights()
