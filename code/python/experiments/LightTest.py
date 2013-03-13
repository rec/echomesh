from __future__ import absolute_import, division, print_function, unicode_literals

import time

LIGHT_COUNT = 5 * 48
LATCH_BYTES = 2
PERIOD = 0.5

ON = bytearray(3 * LIGHT_COUNT + LATCH_BYTES)
OFF = bytearray(3 * LIGHT_COUNT + LATCH_BYTES)

for i in range(3 * LIGHT_COUNT):
  OFF[i] = 0x80
  ON[i] = 0xFF

with open('/dev/spidev0.0', 'wb') as device:
  while True:
    print('ON!')
    device.write(ON)
    device.flush()
    time.sleep(PERIOD)

    print('off')
    device.write(OFF)
    device.flush()
    time.sleep(PERIOD)

