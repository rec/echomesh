from __future__ import absolute_import, division, print_function, unicode_literals

import os.path

from command.RandomCommand import RandomCommand
from command.SequenceCommand import SequenceCommand

from network import Address

from util import File
from util import Log
from util.Closer import Closer
from util.DefaultFile import DefaultFile

LOGGER = Log.logger(__name__)

DEFAULT_DIRECTORY = DefaultFile('score')
DEFAULT_SCORE = 'score.yml'
LOCAL_SCORE = 'local/echomesh-score.yml'
INDEPENDENT_COMMANDS = dict(random=RandomCommand, sequence=SequenceCommand)

class Score(Closer):
  def __init__(self, scorefile, functions, target=Address.NODENAME):
    Closer.__init__(self)
    elements = File.yaml_load_all(LOCAL_SCORE)
    if elements:
      scorefile = LOCAL_SCORE
    else:
      scorefile = DEFAULT_DIRECTORY.expand(scorefile or DEFAULT_SCORE)
      elements = File.yaml_load_all(scorefile)
    LOGGER.info('Loading score %s', DEFAULT_DIRECTORY.relpath(scorefile))
    self.functions = functions
    self.target = target
    self.starters = []
    self.set_elements(elements)

  def start(self):
    for s in self.starters:
      s.start()
      self.add_closer(s)
    self.starters = []

  def set_elements(self, elements):
    self.close_all()
    self.elements = {}
    if elements:
      for r in elements:
        if self.validate_element(r):
          rt = r['type']
          self.elements[rt] = self.elements.get(rt, []) + [r]

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

  def validate_element(self, element):
    ok = True
    for command in element.get('mapping', {}).itervalues():
      cmd = command.get('function', None)
      if cmd not in self.functions:
        ok = False
        LOGGER.error("Didn't understand command %s in element %s", cmd, element)

    if ok:
      cmd = INDEPENDENT_COMMANDS.get(element.get('type', ''), None)
      if cmd:
        self.starters.append(cmd(self, element))

    return ok
