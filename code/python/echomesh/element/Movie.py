from __future__ import absolute_import, division, print_function, unicode_literals

import images2gif

from PIL import Image

from echomesh.element.Repeat import Repeat
from echomesh.util import Log
from echomesh.util.dict.Extract import extract

LOGGER = Log.logger(__name__)

GIF_FIELDS = 'dispose', 'dither', 'nq', 'sub_rectangles'

class Movie(Repeat):
  def __init__(self, parent, description):
    self.filename = description['file']
    if not self.filename.endswith('.gif'):
      self.filename += '.gif'
    description['elements'] = [{'type': 'snapshot', 'file': self.filename[:-4]}]
    self.gif_dict = extract(description, *GIF_FIELDS)
    super(Movie, self).__init__(parent, description, name='Movie')
    self.snapshot = self.elements[0]
    self.gif_dict['duration'] = self.period
    if 'gif_repeats' in description:
      self.gif_dict['repeat'] = description['gif_repeats']

  def _repeat_count_exceeded(self):
    try:
      self.pause()
      def get_file(i):
        return Image.open(self.snapshot.get_file(i + 1)).convert(mode='P')
      images = [get_file(i) for i in range(self.repeat_count)]
      images2gif.writeGif(self.filename, images, **self.gif_dict)
    except:
      LOGGER.error('Unable to write movie file %s', self.filename)

