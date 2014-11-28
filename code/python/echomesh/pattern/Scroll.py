from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.Cechomesh import cechomesh

from echomesh.base import Settings
from echomesh.pattern.Pattern import Pattern

class Scroll(Pattern):
    HELP = 'Scrolls an x,y color list in two dimension.'

    SETTINGS = {
      'dx': {
        'default': 0,
        'help': 'How far, in pixels, to scroll in the x direction.',
        },
      'dy': {
        'default': 0,
        'help': 'How far, in pixels, to scroll in the y direction.',
        },
      'smooth': {
        'default': True,
        'help': ('If true, we interpolate between integer pixels, otherwise '
                 'we jump from pixel to pixel.'),
        },
      'transform': {
        'default': '',
        'help': ('A Transform to apply to dx and dy between pixels.  Only '
                 'useful when smooth=true'),
        },
      'wrap': {
        'default': False,
        'help': ('If true, pixels that are scrolled off the top, bottom, left '
                 'or right reappear at the bottom, top, right or left.'),
        },
      }

    PATTERN_COUNT = 1

    def _evaluate(self):
        color_list = cechomesh.to_color_list(self.patterns()[0])

        columns = (color_list.columns or
                   Settings.get('light', 'visualizer', 'layout')[0])

        return cechomesh.scroll_color_list(
          color_list, self.get('dx'), self.get('dy'), columns=columns,
          wrap=self.get('wrap'), smooth=self.get('smooth'),
          transform=self.get('transform'))
