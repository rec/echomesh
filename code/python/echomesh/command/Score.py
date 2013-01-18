from __future__ import absolute_import, division, print_function, unicode_literals

import os.path

from echomesh.command.Functions import FUNCTIONS
from echomesh.command.RandomCommand import RandomCommand
from echomesh.command.SequenceCommand import SequenceCommand

from echomesh.config import Config

from echomesh.network import Address

from echomesh.util import Log
from echomesh.util.thread import Closer
from echomesh.config import CommandFile
from echomesh.element import Load

LOGGER = Log.logger(__name__)

COMMANDS = dict(random=RandomCommand, sequence=SequenceCommand)

class Score(Closer.Closer):
  def __init__(self, scorefile, makers, parent=None):
    super(Score, self).__init__()
    self.makers = makers
    self.parent = parent
    self.handlers = {}
    self.elements = Load.load_and_make(scorefile, self, makers)

  def add_handler(self, event_type, handler):
    self.handlers[event_type] = handler

  def receive_event(self, event):
    event_type = event.get('subtype', None)
    if event_type:
      for handler in self.handlers.get(event_type, []):
        handler.handle(event)
    else:
      LOGGER.error('No event_type in event %s', event)

  def obsolete_execute_command(self, command, event=None):
    LOGGER.debug('Executing element %s', command)
    function_name = command.get('function', '')
    if not function_name:
      LOGGER.error('No function in command %s', command)
      return

    function = self.makers.get(function_name, None)
    if not function:
      LOGGER.error("Didn't understand function %s", function_name)
      return

    arguments = command.get('arguments', [])
    keywords = command.get('keywords', {})
    self.add_openable(function(self, event, *arguments, **keywords))

def make_score():
  score = Score(Config.get('score', 'file'), FUNCTIONS)
  score.start()
  return score

