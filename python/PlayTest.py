#!/usr/bin/python

import logging
import ossaudiodev
import sys
import wave

LOG_LEVEL = logging.DEBUG
FRAME_SIZE = 65536

def play(filename):
  logging.info('opening file %s', filename)
  sound_file = wave.open(filename,'rb')

  try:
    logging.debug('getting parameters')
    (nc, sw, fr, nf, comptype, compname) = sound_file.getparams()
    logging.debug('parameters were %s', (nc, sw, fr, nf, comptype, compname))

    logging.debug('opening audio')
    sound = ossaudiodev.open('w')
    try:
      logging.debug('setting parameters')
      sound.setparameters(ossaudiodev.AFMT_S16_NE, nc, fr)

      logging.debug('read/write loop')
      data = sound_file.readframes(FRAME_SIZE)
      while data:
        sound.write(data)
        data = sound_file.readframes(FRAME_SIZE)

    finally:
      logging.debug('closing sound device')
      sound.close()

  finally:
    logging.debug('closing file')
    sound_file.close()

if __name__ == '__main__':
  logging.basicConfig(level=LOG_LEVEL)
  if len(sys.argv) is 2:
    play(sys.argv[1])
  else:
    logging.error('Usage: %s filename' % sys.argv[0])
