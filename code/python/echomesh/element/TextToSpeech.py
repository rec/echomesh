from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.element import Element
from echomesh.util import Log
from echomesh.sound import Aplay
from echomesh.sound import GoogleTextToSpeech

LOGGER = Log.logger(__name__)

class TextToSpeech(Element.Element):
  def __init__(self, parent, description):
    super(TextToSpeech, self).__init__(parent, description)
    self.text = description.get('text', '')

  def _on_run(self):
    super(TextToSpeech, self)._on_run()
    self._speak(self.text)

  def handle(self, event):
    self._speak(event.get('text'))

  def _speak(self, text):
    if text:
      f = '(cache failed)'
      try:
        f = GoogleTextToSpeech.CACHE.get_file(text)
        Aplay.play(f)
        self.pause()
      except Exception as e:
        LOGGER.error("Couldn't speak text '%s' from file %s" % (text, f),
                     exc_info=1)

Element.register(TextToSpeech, 'speak')
