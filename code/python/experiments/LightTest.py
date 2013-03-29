#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys
import time

BLACKLIST_FILE = '/etc/modprobe.d/raspi-blacklist.conf'
BLACKLIST_TEMP = BLACKLIST_FILE + '.tmp'

PERM_ERROR = """
This script needs to be run as superuser (because it writes to the SPI driver).
Please rerun it as follows:

  sudo %s
"""

FIX_BLACKLIST_PROMPT = """
The SPI service has been blacklisted on your distribution.

Would you like to fix it now?  You'll need to restart your Raspberry Pi
for the changes to take effect.
"""

DEFAULT_LIGHT_COUNT = 128
DEFAULT_REPEAT_COUNT = 2

PERIOD = 0.5

LATCH_BYTE_COUNT = 2

LIGHT_COUNT = DEFAULT_LIGHT_COUNT if len(sys.argv) == 1 else int(sys.argv[1])
REPEAT_COUNT = DEFAULT_REPEAT_COUNT if len(sys.argv) < 3 else int(sys.argv[2])
BYTE_COUNT = 3 * LIGHT_COUNT + LATCH_BYTE_COUNT


def _test_su():
  if os.geteuid():
    raise Exception(PERM_ERROR % ' '.join(sys.argv))

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


def _speedup():
  try:
    import spidev
    spi = spidev.SpiDev()
  except:
    print("Couldn't speed up SPI, please install py-spidev")
  else:
    spi.open(0, 0)
    spi.max_speed_hz = 20000000


def _blacklist():
  if _is_blacklisted():
    result = raw_input('Fix now? (y/N)')
    if result.lower().startswith('y'):
      _fix_blacklist()
      print('Your blacklist has been fixed.  Please restart your Raspberry Pi\n'
            'and run this program again!')
      return True
    else:
      raise Exception("SPI is blacklisted, can't run lights on your machine.")
  else:
    print('SPI is not blacklisted.')

def _light_array(x=0x80):
  b = bytearray(x for i in xrange(BYTE_COUNT))
  for i in range(LATCH_BYTE_COUNT):
    b[-1 - i] = 0
  return b

def _get_off_on():
  return _light_array(), _light_array(0xff)

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

def _stream_lights(reverse=False):
  with open('/dev/spidev0.0', 'wb') as device:
    lights = _light_array()
    old = 0
    for i in range(LIGHT_COUNT):
      index = LIGHT_COUNT - i -1 if reverse else i
      lights[3 * index: 3 * (index + 1)] = [0xFF, 0xFF, 0xFF]
      if i:
        lights[3 * old: 3 * (old + 1)] = [0x80, 0x80, 0x80]
      old = index
      device.write(lights)
      device.flush()
    lights[3 * old: 3 * (old + 1)] = [0x80, 0x80, 0x80]
    device.write(lights)
    device.flush()

def _stream_lights2(reverse=False):
  on = bytearray(0xff for i in range(3))
  off = bytearray(0x80 for i in range(3))
  latch = bytearray(0 for i in range(LATCH_BYTE_COUNT))
  with open('/dev/spidev0.0', 'wb') as device:
    for i in range(LIGHT_COUNT):
      for j in range(LIGHT_COUNT):
        index = LIGHT_COUNT - j -1 if reverse else j
        device.write(on if i == index else off)
      device.write(latch)
      device.flush()

    for j in range(LIGHT_COUNT):
      device.write(off)
    device.write(latch)
    device.flush()

def test_lights():
  try:
    _test_su()
    if not _blacklist():
      _speedup()
      _flash_lights()
      for i in range(REPEAT_COUNT):
        stream = _stream_lights if i % 2 else _stream_lights2
        stream()
        stream(reverse=True)

  except Exception as e:
    print('ERROR:', e)
    raise
    exit(-1)


if __name__ == '__main__':
  test_lights()
