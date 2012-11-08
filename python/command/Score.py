from __future__ import absolute_import, division, print_function, unicode_literals

import os.path

from command.RandomCommand import RandomCommand

from network import Address

from util import File
from util import Log
from util.Closer import Closer
from util.DefaultFile import DefaultFile

LOGGER = Log.logger(__name__)

DEFAULT_DIRECTORY = DefaultFile('~/echomesh/score')
DEFAULT_SCORE = 'score.yml'
LOCAL_SCORE = os.path.expanduser('~/.echomesh-score')

class Score(Closer):
  def __init__(self, scorefile, functions, target=Address.NODENAME):
    Closer.__init__(self)
    rules = File.yaml_load_all(LOCAL_SCORE)
    if not rules:
      scorefile = DEFAULT_DIRECTORY.expand(scorefile or DEFAULT_SCORE)
      rules = File.yaml_load_all(scorefile)
    self.functions = functions
    self.target = target
    self.set_rules(rules)

  def set_rules(self, rules):
    self.close_all()
    self.rules = {}
    if rules:
      for r in rules:
        if self.validate_rule(r):
          rt = r['type']
          self.rules[rt] = self.rules.get(rt, []) + [r]

  def receive_event(self, event):
    rules = self.rules.get(event['event'], None)
    for r in rules:
      if (r
          and r.get('source', self.target) == event.get('source', self.target)
          and r.get('target', self.target) == self.target):
        self.execute_rule(r, event)

  def execute_rule(self, rule, event):
    LOGGER.debug('Executing rule %s', rule)
    key = event.get('key', {})
    mapping = rule.get('mapping', {})
    command = mapping.get(key, {})
    function_name = command.get('function', {})
    function = self.functions.get(function_name, None)
    if function:
      arguments = command.get('arguments', [])
      keywords = command.get('keywords', {})
      closer = function(self, event, *arguments, **keywords)
      if closer:
        self.add_closer(closer)
    else:
      LOGGER.error("Didn't understand function %s", function_name)

  def validate_rule(self, rule):
    ok = True
    for command in rule.get('mapping', {}).itervalues():
      cmd = command.get('function', None)
      if cmd not in self.functions:
        ok = False
        LOGGER.error("Didn't understand command %s in rule %s", cmd, rule)

    if ok:
      if rule.get('type', '') == 'random':
        rand = RandomCommand(self, rule)
        self.add_closer(rand)
        rand.start()

    return ok
