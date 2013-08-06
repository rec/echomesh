from __future__ import absolute_import, division, print_function, unicode_literals

def decorator(fn):
  print(fn.__name__)
  return fn

@decorator
def hello():
  print('hello, world')


hello()
