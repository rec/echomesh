from __future__ import absolute_import, division, print_function, unicode_literals

import random

from graphics.Sprite import ImageSprite
from sound.FilePlayer import FilePlayer
from util import Log

LOGGER = Log.logger(__name__)

def select_random(score, event, *choices):
  if choices:
    item = random.choice(choices)
    if item:
      function_name, args = item[0], item[1:]
      function = score.functions.get(function_name, None)
      if function:
        function(score, event, *args)
      else:
        LOGGER.error('No function named "%s": %s, %s', function_name, item, choices)
    else:
      LOGGER.error('No choices for select_random')
  else:
    LOGGER.error('No arguments to select_random')

def print_function(score, event, *args):
  print(*args)

def play_audio(score, event, *args):
  if not args:
    LOGGER.error('No arguments for play_audio')
  else:
    if len(args) > 1:
      LOGGER.warning('Extra arguments to play_audio discarded')
    try:
      player = FilePlayer(**args[0])
      player.start()
      return player
    except:
      LOGGER.error("Didn't understand play_audio arguments %s", args[0])

def functions(display):
  def play_image(score, event, **keywords):
    filename = keywords.get('image', None)
    if filename:
      keywords['image'] = display.textures.loadTexture(filename)
      display.add_sprite(ImageSprite(**keywords))
    else:
      LOGGER.error('No filename in image arguments %s', keywords)

  return dict(random=select_random,
              print=print_function,
              audio=play_audio,
              image=play_image)

