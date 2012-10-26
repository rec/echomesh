from __future__ import absolute_import, division, print_function, unicode_literals

from command import RandomCommand

from util import Closer
from util import Log
from util.Openable import Openable
from util.RandomCommand import Openable

LOGGER = Log.LOGGER(__name__)

class Score(Openable):
  def __init__(self, rules, commands, target):
    self.rules = {}
    self.commands = commands
    self.target = target
    self.closers = Closer.Closer()
    for r in rules:
      if self.validate_rule(r):
        rt = r['type']
        self.rules[rt] = self.rules.get(rt, []) + [r]

  def close(self):
    Openable.close(self)
    self.closers.close()

  def receive_event(self, event):
    rule = self.rules.get(event['type'], None)

    if (rule
        and rule.get('source', self.target) == event.get('source', self.target)
        and rule.get('target', self.target) == self.target):
      self.execute_rule(rule, event.get('key', {}))

  def execute_rule(self, rule, key):
    mapping = rule.get('mapping', {})
    command = mapping.get(key, {})
    command_name = command.get('command', {})
    function = self.commands.get(command_name, None)
    if function:
      for args in command.get('arguments', []):
        closer = function(*args)
        if closer:
          self.closers.add_closer(closer)
    else:
      LOGGER.error("Didn't understand command name %s", command_name)

  def validate_rule(self, rule):
    ok = True
    for command in rule.get('mapping', {}).itervalues():
      cmd = command.get('command', None)
      if cmd not in self.commands:
        ok = False
        LOGGER.error("Didn't understand command %s in rule %s", cmd, rule)

    if rule.get('type', '') == 'random':
      rand = RandomCommand(self, rule)
      self.randoms.add_closer(rand)
      rand.start
