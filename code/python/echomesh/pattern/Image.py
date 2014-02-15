from __future__ import absolute_import, division, print_function, unicode_literals

import cechomesh

from echomesh.util.image import Resize
from echomesh.util import Log
from echomesh.pattern.Pattern import Pattern

LOGGER = Log.logger(__name__)

class Image(Pattern):
  CONSTANTS = 'filename', 'x', 'y',
  OPTIONAL_CONSTANTS = {'top': None, 'left': None, 'stretch': False}
  PATTERN_COUNT = 0

  def _evaluate(self):
    parts = self.get_all('filename', 'x', 'y', 'stretch', 'top', 'left')
    return cechomesh.ColorList(Resize.resize(*parts).getdata())
