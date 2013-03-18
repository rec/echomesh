#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys
import time

PERM_ERROR = """
This script needs to be run as superuser (because it writes to the SPI driver).
Please rerun it as follows:

  %s
"""

if os.geteuid():
  print(PERM_ERROR % ' '.join(['su'] + sys.argv))
  exit(-1)

LIGHT_COUNT = 12  # 5 * 48
LATCH_BYTE_COUNT = 0  # 2
PERIOD = 0.5
LATCH_BYTES = bytearray(b'\x00\x00\x00')

ON = bytearray(3 * LIGHT_COUNT + LATCH_BYTE_COUNT)
OFF = bytearray(3 * LIGHT_COUNT + LATCH_BYTE_COUNT)

for i in range(3 * LIGHT_COUNT):
  OFF[i] = 0x80
  ON[i] = 0xFF

print(ON)
print(OFF)

with open('/dev/spidev0.0', 'wb') as device:
  def write(data, name):
    device.write(data)
    device.flush()
    device.write(LATCH_BYTES)
    device.flush()
    print(name)
    time.sleep(PERIOD)

  while True:
    write(ON, 'ON!')
    write(OFF, 'off')
