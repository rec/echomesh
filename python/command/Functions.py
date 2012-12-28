from __future__ import absolute_import, division, print_function, unicode_literals

import random
import traceback

from config import Config
from util import Closer
from util import Log

LOGGER = Log.logger(__name__)

FUNCTIONS = {}

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

def play_image(score, event, **keywords):
  if Config.is_enabled('display'):
    from graphics.Sprite import ImageSprite
    ImageSprite(**keywords)
  else:
    LOGGER.info('Playing image %s', keywords.get('image', '(none)'))

def play_audio(score, event, **keywords):
  if Config.is_enabled('audio', 'output'):
    from sound import FilePlayer
    player = FilePlayer.play(**keywords)
    if player:
      player.start()
      Closer.close_on_exit(player)
  else:
    LOGGER.info('Playing audio')

def register(**kwds):
  for name, function in kwds.iteritems():
    if name in FUNCTIONS:
      LOGGER.error('Duplicate function name %s', name)
    FUNCTIONS[name] = function

register(audio=play_audio,
         image=play_image,
         print=print_function,
         random=select_random,
         )
