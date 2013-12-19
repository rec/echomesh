from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Log

LOGGER = Log.logger(__name__)

class ClientSingleton(object):
  def __init__(self):
    self.client = None
    self.owner_count = 0

  def add_owner(self):
    self.client = self.client or self.make_client()
    self.owner_count += 1

  def remove_owner(self):
    self.owner_count -= 1
    if not self.owner_count:
      self.client = None
