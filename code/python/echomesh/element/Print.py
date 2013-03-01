from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Log
from echomesh.element import Element

LOGGER = Log.logger(__name__)

class Print(Element.Element):
  def __init__(self, parent, description):
    super(Print, self).__init__(parent, description)
    self.text = description.get('text', '')

  def _on_run(self):
    super(Print, self)._on_run()
    try:
      text = self.text.format(**self.__dict__)
    except:
      text = self.text
    LOGGER.info(text)
    self.stop()

  def handle(self, event):
    LOGGER.info('%s: %s', self.text, event)

Element.register(Print)
