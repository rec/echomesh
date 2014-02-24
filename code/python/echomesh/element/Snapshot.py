from __future__ import absolute_import, division, print_function, unicode_literals

import os.path

from echomesh.element.Element import Element
from echomesh.output.Visualizer import Visualizer
from echomesh.util import Log

LOGGER = Log.logger(__name__)

LEGAL_FILE_SUFFIXES = frozenset(['.jpeg', '.jpg', '.png'])

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
    Visualizer.INSTANCE.snapshot(self.get_file(self.index))

  def get_file(self, index):
    if self.use_index:
      if self.use_format:
        return self.root % index + self.ext
      else:
        return '%s-%s%s' % (self.root, index, self.ext)
    else:
      return self.root + self.ext

