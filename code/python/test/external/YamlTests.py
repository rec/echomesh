"""

>>> read = FakeRead()
>>> write = FakeWrite()


"""

import yaml

INPUT = """\
a: 4
---
b: 5
---
c: 6
___
___
___
d: 7

"""

def FakeRead(object):
  def __init__(self, *items):
    self.name = 'read'
    self.items = items or INPUT.split('\n')

  def read(self, *args, **kwds):
    print('read', name, args, kwds)
    return items.pop(0) if items else None

def FakeWrite(object):
  def __init__(self, name=''):
    self.name = name

  def write(self, data):
    print('write', name, data)
    return items.pop(0) if items else None
