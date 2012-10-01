#!/usr/bin/python

from datetime import datetime
from math import sqrt

import time

WAIT_TIME = 0.050
ITERATIONS = 100

# Copied from http://www.physics.rutgers.edu/~masud/computing/WPark_recipes_in_python.html

def meanstdv(x):
  n, mean, std = len(x), 0, 0
  for a in x:
    mean = mean + a
  mean = mean / float(n)

  for a in x:
    std = std + (a - mean)**2
  std = sqrt(std / float(n-1))

  return mean, std

# Copied from http://stackoverflow.com/questions/1133857/how-accurate-is-pythons-time-sleep

def sleepError(amount=WAIT_TIME):
  start = datetime.now()
  time.sleep(amount)
  end = datetime.now()
  delta = end - start
  return abs((delta.seconds + delta.microseconds / 1000000.) - amount)

errors = [1000. * sleepError() for i in xrange(ITERATIONS)]
print 'Error: average %0.2fms; std dev %0.2fms' % meanstdv(errors)
