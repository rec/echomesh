from __future__ import absolute_import, division, print_function, unicode_literals

import random

from sound.FilePlayer import FilePlayer
from util import Log

LOGGER = Log.logger(__name__)

def select_random(score, event, *choices):
  if choices:
    item = random.choice(choices)
    function_name = item.get('function', None)
    function = score.functions.get(function_name, None)
    if function:
      keywords = item.get('keywords', {})
      arguments = item.get('arguments', [])
      function(score, event, *arguments, **keywords)
    else:
      LOGGER.error('No function named "%s": %s, %s', function_name, item, choices)
  else:
    LOGGER.error('No arguments to select_random')

def print_function(score, event, *args):
  print(*args)

def functions(echomesh, display):
  if echomesh.config['display'].get('enable', True):
    from graphics.Sprite import ImageSprite

    def play_image(score, event, **keywords):
      ImageSprite(display, **keywords)
  else:
    def play_image(score, event, **keywords):
      LOGGER.info('Playing an image')

  def play_audio(score, event, **keywords):
    try:
      player = FilePlayer(**keywords)
      player.start()
      echomesh.add_closer(player)
      return player
    except:
      LOGGER.error("Didn't understand play_audio arguments %s", args[0])

  return dict(
    audio=play_audio,
    image=play_image,
    print=print_function,
    select=select_random,
    )

