#!/usr/bin/python

import datetime
import math
import sys
import time

ITERATIONS = 10
MICROSECONDS_PER_SECOND = 1000000.
PRESKIP = 0
USAGE = 'Usage: TestSleepAccuracy [iterations] [waitTimeInFloatingPointSeconds]'
WAIT_TIME = 0.005

# Copied from http://www.physics.rutgers.edu/~masud/computing/WPark_recipes_in_python.html

def meanstdv(x):
  n, mean, std = len(x), 0, 0
  for a in x:
    mean = mean + a
  mean = mean / float(n)

  for a in x:
    std = std + (a - mean)**2
  std = math.sqrt(std / float(n-1))

  return mean, std

def sleepError(wait):
  start = datetime.datetime.now()
  time.sleep(wait)
  end = datetime.datetime.now()
  delta = end - start
  error = (delta.seconds + delta.microseconds / MICROSECONDS_PER_SECOND) - wait
  if error < 0:
    print 'UNDERRUN:', error  # Never happens.
    error = -error

  return error

def getSleepErrors(iterations=ITERATIONS, t=WAIT_TIME):
  return [MICROSECONDS_PER_SECOND * sleepError(t) for i in xrange(iterations)]

def reportSleepErrors(errors, iterations=ITERATIONS, t=WAIT_TIME):
  print '%d iterations, wait %dus' % (iterations, t * MICROSECONDS_PER_SECOND)
  print '  average %dus; std dev %dus' % meanstdv(errors)
  print '  min: %dus, max: %dus' % (min(errors), max(errors))

def runSleepReport(iterations=ITERATIONS, wait=WAIT_TIME):
  wait = float(wait)
  iterations = int(iterations)
  if PRESKIP:
    # Skipping the first few to get stability seems to have no effect.
    getSleepErrors(PRESKIP, wait)

  reportSleepErrors(getSleepErrors(iterations, wait), iterations, wait)

if __name__ == '__main__':
  if len(sys.argv) <= 3:
    runSleepReport(*sys.argv[1:])
  else:
    print USAGE
