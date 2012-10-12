import alsaaudio
import numpy
import analyse

card = 'sysdefault:CARD=AK5370'
f = open('out.wav', 'wb')
inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, card)

inp.setchannels(1)
inp.setrate(44000)
inp.setperiodsize(160)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)

while True:
  length, data = inp.read()

  samps = numpy.fromstring(data, dtype=numpy.int16, count=length)
  # Show the volume and pitch
  print analyse.loudness(samps), analyse.musical_detect_pitch(samps)
