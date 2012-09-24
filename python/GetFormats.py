#!/usr/bin/python
import ossaudiodev

sound = ossaudiodev.open('w')
fmts = sound.getfmts()

for name in dir(ossaudiodev):
  if name.startswith('AFMT'):
    attr = getattr(ossaudiodev, name)
    if attr & fmts:
      print name
