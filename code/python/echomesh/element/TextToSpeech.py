from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.element import Element
from echomesh.util import Log
from echomesh.sound import GoogleTextToSpeech

LOGGER = Log.logger(__name__)

class TextToSpeech(Element.Element):
  def _on_start(self):
    self.handle(self.description)

  def handle(self, event):
    text = event.get('text')
    if text:
      try:
        filename = GoogleTextToSpeech.to_speech_file(text)
      except Exception as e:
        LOGGER.error("Couldn't speak text '%s', exception %s" % (text, e))


Element.register(TextToSpeech)
