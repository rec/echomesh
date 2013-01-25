from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Log
from echomesh.util.thread.RunnableOwner import RunnableOwner

LOGGER = Log.logger(__name__)

class Element(RunnableOwner):
  def __init__(self, parent, description):
    super(Element, self).__init__()
    self.parent = parent
    self.description = description

