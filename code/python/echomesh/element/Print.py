from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.config import Config
from echomesh.util import Log
from echomesh.element import Element

LOGGER = Log.logger(__name__)

class Print(Element.Element):
  def __init__(self, parent, description):
    super(Print, self).__init__(parent, description)

  def start(self):
    super(Print, self).start()
    LOGGER.info(descriptionn)

Element.register(Print)
