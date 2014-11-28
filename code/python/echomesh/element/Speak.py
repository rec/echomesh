from __future__ import absolute_import, division, print_function, unicode_literals

import copy

from echomesh.element import Element
from echomesh.sound import GoogleTextToSpeech
from echomesh.sound.CPlayer import CPlayer
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class Speak(Element.Element):
    def __init__(self, parent, description):
        super(Speak, self).__init__(parent, description)
        self.player_description = copy.copy(description)
        self.text = self.player_description.pop('text', '')

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
            player = CPlayer(self, file=f, **self.player_description)
            self.add_mutual_pause_slave(player)
            player.run()
