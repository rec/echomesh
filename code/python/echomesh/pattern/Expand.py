from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.Cechomesh import cechomesh

from echomesh.base import Settings
from echomesh.pattern.Pattern import Filter
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class Expand(Filter):
    HELP = """Expand an image."""

    SETTINGS = {
      'scale': {
        'default': [1, 1],
        'help': ('How much to expand each pixel in the x and y directions.'),
        },
      }

    def _evaluate_one(self, color):
        return cechomesh.expand_color_list(colors, *self.get(scale))
