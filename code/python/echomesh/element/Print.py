from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Config
from echomesh.util import Log
from echomesh.element import Element
from echomesh.element import Register

LOGGER = Log.logger(__name__)

class Print(Element.Element):
  def __init__(self, parent, description):
    super(Print, self).__init__(parent, description)

  def start(self):
    super(Print, self).start()
    LOGGER.info(self.description)

  def handle(self, event):
    LOGGER.info(event)

Register.register(Print)
