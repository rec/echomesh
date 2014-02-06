from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.element import Element
from echomesh.sound import GoogleTextToSpeech
from echomesh.sound import Play
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class Speak(Element.Element):
  def __init__(self, parent, description):
    super(Speak, self).__init__(parent, description)
    self.text = description.get('text', '')

  def _on_run(self):
    super(Speak, self)._on_run()
    self._speak(self.text)

  def handle(self, event):
    # TODO: this won't work.
    self._speak(event.get('text'))

  def _speak(self, text):
    assert text, 'Speak element has no text'
    try:
      f = GoogleTextToSpeech.CACHE.get_file(text)
    except Exception:
      LOGGER.error("Couldn't speak text '%s' from file %s", text, f,
                     exc_info=1)
      self.pause()
    else:
      player = Play.play(self, file=f, **self.description)
      self.add_mutual_pause_slave(player)
      player.run()
