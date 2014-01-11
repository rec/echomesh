from __future__ import absolute_import, division, print_function, unicode_literals

import os.path

from echomesh.element.Element import Element
from echomesh.output.Visualizer import Visualizer
from echomesh.util import Log

LOGGER = Log.logger(__name__)

LEGAL_FILE_SUFFIXES = '.png', '.jpg', '.jpeg'

class Snapshot(Element):
  def __init__(self, parent, description):
    super(Snapshot, self).__init__(parent, description, name='Snapshot')
    self.use_index = description.get('use_index', True)
    filename = description['file']
    self.use_format = description.get('use_format', '%' in filename)
    self.index = 0
    self.root, self.ext = os.path.splitext(filename)
    self.ext = self.ext or '.png'
    if self.ext not in LEGAL_FILE_SUFFIXES:
      raise Exception(
        'Illegal file extension %s for snapshot: legal extensions are %s' %
        (self.ext, ' '.join(LEGAL_FILE_SUFFIXES)))

  def _on_run(self):
    super(Snapshot, self)._on_run()

    if not Visualizer.INSTANCE:
      LOGGER.error('No Visualizer.INSTANCE')
      return

    self.pause()
    self.index += 1
    if self.use_index:
      if self.use_format:
        f = self.root % self.index + self.ext
      else:
        f = '%s-%s%s' % (self.root, self.index, self.ext)
    else:
      f = self.root + self.ext
    Visualizer.INSTANCE.snapshot(f)
