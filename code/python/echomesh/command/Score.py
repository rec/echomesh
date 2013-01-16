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
from echomesh.command import Element

LOGGER = Log.logger(__name__)

COMMANDS = dict(random=RandomCommand, sequence=SequenceCommand)

class Score(Closer.Closer):
  def __init__(self, scorefile, functions, target=Address.NODENAME):
    super(Score, self).__init__()
    self.functions = functions
    self.target = target
    self.score_by_type = {}

    for element in CommandFile.load('score', scorefile):
      if not Element.validate(element, self.functions):
        LOGGER.error("Didn't understand command %s in element %s", cmd, element)
        continue

      t = element.get('type', None)
      if not t:
        LOGGER.error('No type field in element')
        continue

      self.score_by_type[t] = self.score_by_type.get(t, []) + [element]
      f = self.functions.get(t, None)
      self.add_openable(f and f(self, element))

  def receive_event(self, event):
    elements = self.elements.get(event['event'], [])
    for e in elements:
      if (e
          and e.get('source', self.target) == event.get('source', self.target)
          and e.get('target', self.target) == self.target):
        key = event.get('key', {})
        mapping = element.get('mapping', {})
        command = mapping.get(key, {})
        self.execute_command(command, event)

  def execute_command(self, command, event=None):
    if command:
      LOGGER.debug('Executing element %s', command)
      function_name = command.get('function', '')
      if not function_name:
        LOGGER.error('No function in command %s', command)
        if True:
          raise Exception
        return

      function = self.functions.get(function_name, None)
      if not function:
        LOGGER.error("Didn't understand function %s", function_name)
        return

      arguments = command.get('arguments', [])
      keywords = command.get('keywords', {})
      closer = function(self, event, *arguments, **keywords)
      if closer:
        self.add_closer(closer)

def make_score():
  score = Score(Config.get('score', 'file'), FUNCTIONS)
  score.start()
  return score

