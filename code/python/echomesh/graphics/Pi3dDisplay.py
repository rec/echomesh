from __future__ import absolute_import, division, print_function, unicode_literals

import time

from echomesh.base import Settings
from echomesh.expression import Expression
from echomesh.graphics import Shader
from echomesh.util.thread import Runnable

class Pi3dDisplay(Runnable.Runnable):
    def __init__(self):
        super(Pi3dDisplay, self).__init__()
        self.timeout = Expression.convert(Settings.get('network', 'timeout'))
        keywords = {}

        background = Settings.get('pi3d', 'background')
        if background:
            keywords.update(background=background)

        dimensions = Settings.get('pi3d', 'dimensions')
        if dimensions:
            x, y, width, height = dimensions
            keywords.update(x=x, y=y, width=width, height=height)

        for k in ['aspect', 'depth', 'far', 'near', 'tk', 'window_title']:
            keywords[k] = Settings.get('pi3d', k)

        from pi3d import Display
        self.display = Display.create(**keywords)
        Settings.add_client(self)
        Shader.SHADER()
        # Make sure that the shader is created in the main thread!

    def settings_update(self, get):
        if self.display:
            self.display.frames_per_second = get('pi3d', 'frames_per_second')

    def _on_run(self):
        super(Pi3dDisplay, self)._on_run()
        self.display.first_time = True
        self.display.is_running = True

    def _on_pause(self):
        super(Pi3dDisplay, self)._on_pause()
        self.display.stop()

    def loop(self):
        while self.is_running:
            if not self.display.loop_running():
                self.pause()
