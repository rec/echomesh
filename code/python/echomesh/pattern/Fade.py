from __future__ import absolute_import, division, print_function, unicode_literals

import cechomesh

from echomesh.pattern.Pattern import Pattern

class Fade(Pattern):
  HELP = 'Fade between zero or more patterns.'

  SETTINGS = {
    'fade': {
      'default': 0.0,
      'help': ('Controls which pattern is seen.  At 0.0, the first pattern is '
               'seen, at 1.0 the last pattern is seen.'),
      },
    }

  def _evaluate(self):
    patterns = self.patterns()
    if not patterns:
      return []
    steps = len(patterns) - 1
    if not steps:
      return patterns[0]

    fade_value = self.get('fade')
    total_fade = fade_value * steps
    segment = int(total_fade)
    fade = total_fade - segment
    if segment < steps:
      p1, p2 = patterns[segment], patterns[segment + 1]
      return cechomesh.to_color_list(p1).interpolate(p2, fade)
    else:
      return patterns[segment]
