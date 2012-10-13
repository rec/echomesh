import alsaaudio

card = 'sysdefault:CARD=AK5370'
inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, card)
inp.setchannels(1)
inp.setrate(44000)
inp.setperiodsize(160)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)

i = 250
while i > 0:
  length, data = inp.read()
  if i is 250:
    print data
  f.write(data)
  i -= 1
