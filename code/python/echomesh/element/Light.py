from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Log
from echomesh.element import Sequence
from echomesh.element import Scene

LOGGER = Log.logger(__name__)

class Light(Sequence.Sequence):
  def __init__(self, parent, description):
    super(Light, self).__init__(parent, description)
    scenes = description.get('scenes', {}).iteritems()
    self.scenes = dict((k, Scene.scene(v)) for k, v in scenes)


Element.register(Light)

