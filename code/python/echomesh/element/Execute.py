from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Log
from echomesh.element import Element

LOGGER = Log.logger(__name__)

class Execute(Element.Element):
  def __init__(self, parent, description):
    super(Execute, self).__init__(parent, description)
    self.binary = description['binary']

  def _on_run(self):
    super(Execute, self)._on_run()
    try:
      text = self.text.format(**self.__dict__)
    except:
      text = self.text
    LOGGER.info(text)
    return True  # Request to pause the Element.

  def handle(self, event):
    LOGGER.info('%s: %s', self.text, event)

