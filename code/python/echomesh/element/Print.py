from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Config
from echomesh.util import Log
from echomesh.element import Element
from echomesh.element import Register

LOGGER = Log.logger(__name__)

class Print(Element.Element):
  def __init__(self, parent, description):
    super(Print, self).__init__(parent, description)

  def run(self):
    super(Print, self).run()
    LOGGER.info(descriptionn)

Register.register(Print)
