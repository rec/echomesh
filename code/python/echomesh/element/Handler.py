from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Log
from echomesh.element import Element

LOGGER = Log.logger(__name__)

class Handler(Element.Element):
    def __init__(self, parent, description):
        super(Handler, self).__init__(parent, description)
        self.handler_parent = None
        self.event_type = description.get('event_type')

    def _on_run(self):
        super(Handler, self)._on_run()
        handler = self.get_property('add_handler')
        if handler:
            self.handler_parent = handler
            handler.add_handler(self)
        else:
            LOGGER.warning("Didn't find a handler parent in open for %s", self)

    def _on_pause(self):
        super(Handler, self)._on_pause()
        if hasattr(self.handler_parent, 'remove_handler'):
            self.handler_parent.remove_handler(self)
        else:
            LOGGER.warning("Didn't find a handler parent in close for %s", self)
