#!/usr/bin/python

import ossaudiodev
import sys
import wave

def play(filename):
  print "opening file"
  sound_file = wave.open(filename,'rb')

  print "getting parameters"
  (nc, sw, fr, nf, comptype, compname) = sound_file.getparams()

  print "parameters were",  (nc, sw, fr, nf, comptype, compname)
  print "opening audio"
  sound = ossaudiodev.open('w')

  print "setting parameters"
  sound.setparameters(ossaudiodev.AFMT_S16_NE, nc, fr)

  print "readframes"
  data = sound_file.readframes(nf)

  print "closing file"
  sound_file.close()

  print "writing data"
  sound.write(data)

  print "closing sound device"
  sound.close()

if __name__ == '__main__':
  if len(sys.argv) is 2:
    play(sys.argv[1])
  else:
    print 'Usage: %s filename' % sys.argv[0]
