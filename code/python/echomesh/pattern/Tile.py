from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.Cechomesh import cechomesh

from echomesh.base import Settings
from echomesh.pattern.Pattern import Filter
from echomesh.util import Log

LOGGER = Log.logger(__name__)
_CENTERING = {'begin': -1, 'center': 0, 'end': -1}

class Tile(Filter):
    HELP = """Tile an array inside a large array."""

    SETTINGS = {
      'scale': {
        'default': None,
        'help': ('How much to multiply the size in the x and y directions.'),
        },

      'size': {
        'default': None,
        'help': ('The final [x, y] size, in pixels.'),
        },

      'center': {
        'default': ['begin', 'begin'],
        'help': ('Where to center on the x and y axes.  '
                 'Valid choices are begin, middle, end - or a negative number, '
                 'zero or a positive number.'),
        },
      }

    PATTERN_COUNT = 1

    def _evaluate_one(self, color_list):
        if not color_list:
            LOGGER.error('Empty input to Tile.')
            return color_list

        size = self.get('size')
        scale = self.get('scale')

        if scale:
            if size:
                LOGGER.warn('Ignoring scale in Tile pattern that has a size')
            else:
                columns = color_list.columns or len(color_list)
                rows = cechomesh.compute_rows(len(color_list), columns)
                size = [int(scale[0] * columns), int(scale[1] * rows)]
        elif not scale:
            LOGGER.error('No size or scale for Tile pattern.')
            return color_list

        center = [_CENTERING.get(c, c) for c in self.get('center')]
        return cechomesh.tile_colors(color_list, *(size + center))
