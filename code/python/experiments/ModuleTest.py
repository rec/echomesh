from __future__ import absolute_import, division, print_function, unicode_literals

def f():
  pass

try:
  print(dir(f.__module__))
except:
  print('f has no module')

class G(object):
  pass

g = G()

try:
  print(g.__module__)
except:
  print('g has no module')

try:
  print(G.__module__)
except:
  print('G has no module')



