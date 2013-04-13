from __future__ import absolute_import, division, print_function, unicode_literals

import time
import yaml

# Setting either or both of these to true makes no difference to the results.
IS_SAFE = False
USE_SLEEP = False

load_all = yaml.safe_load_all if IS_SAFE else yaml.load_all
dump_all = yaml.safe_dump_all if IS_SAFE else yaml.dump_all

def send():
  for i in range(3):
    print('send', i)
    yield i
    if USE_SLEEP:
      time.sleep(0.5)

for i in load_all(dump_all(send())):
  print('receive', i)

# Result:
#
#   send 0
#   send 1
#   send 2
#   receive 0
#   receive 1
#   receive 2

