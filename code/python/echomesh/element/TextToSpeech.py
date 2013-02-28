from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.element import Element
from echomesh.util import Log
from echomesh.sound import Aplay
from echomesh.sound import GoogleTextToSpeech

LOGGER = Log.logger(__name__)

class TextToSpeech(Element.Element):
  def _on_run(self):
    self.handle(self.description)

  def handle(self, event):
    text = event.get('text')
    if text:
      f = '(cache failed)'
      try:
        f = GoogleTextToSpeech.CACHE.get_file(text)
        Aplay.play(f)
        self.stop()
      except Exception as e:
        LOGGER.error("Couldn't speak text '%s' from file %s" % (text, f),
                     exc_info=1)

Element.register(TextToSpeech, 'speak')
