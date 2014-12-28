from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.output import Visualizer

def window(_, command='open'):
    if command not in ('close', 'open'):
        raise Exception('Don\'t understand command "window %s"' % command)
    Visualizer.set_visible(command == 'open')

HELP = """
  Open or close the current window.

Examples:
  window
  window open
  window close
"""
