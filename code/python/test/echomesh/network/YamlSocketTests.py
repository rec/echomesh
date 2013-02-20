"""

"""

from __future__ import absolute_import, division, print_function, unicode_literals

class MockReadWriteSocket(object):
  def __init__(self, *data):
    self.data = list(data)

  def recv(

