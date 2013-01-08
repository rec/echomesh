from __future__ import absolute_import, division, print_function, unicode_literals

import os.path

from echomesh.network import Address

from echomesh.util.DefaultFile import DefaultFile
from echomesh.util import File
from echomesh.util import Log

LOGGER = Log.logger(__name__)

DEFAULT_ELEMENT_DIRECTORY = DefaultFile('element')

DEFAULT_SCORE_FILE = 'score.yml'

def _score_file(node, scorefile):
  if not scorefile.endswith('.yml'):
    scorefile += '.yml'
  return os.path.join('nodes', node, 'score', *scorefile.split('/'))

def _get_score_file(scorefile):
  for node in ['local', Address.NODENAME, 'global']:
    f = _score_file(node, scorefile)
    if os.path.exists(f):
      return f

def resolve_element(element):
  filename = element.get('filename', None)
  if filename:
    return File.yaml_load(DEFAULT_ELEMENT_DIRECTORY.expand(filename))
  else:
    return element

class ScoreReader(object):
  def __init__(self, score, commands):
    self.score = score
    self.commands = commands

  def read(self, elements):
    result = {}
    starters = []
    for e in elements:
      ok, starter = self.validate_element(resolve_element(e))
      if ok:
        if starter:
          starters.append(starter)
        t = e['type']
        result[t] = result.get(t, []) + [e]
    return result, starters

  def validate_element(self, element):
    ok, starter = True, None
    for command in element.get('mapping', {}).itervalues():
      cmd = command.get('function', None)
      if cmd not in self.score.functions:
        ok = False
        LOGGER.error("Didn't understand command %s in element %s", cmd, element)

    if ok:
      cmd = self.commands.get(element.get('type', ''), None)
      starter = cmd and cmd(self.score, element)

    return ok, starter

def load_score_elements(scorefile):
  f = _get_score_file(scorefile or DEFAULT_SCORE_FILE)
  if f:
    LOGGER.info('Loading score %s', f)
    return File.yaml_load_all(f)
  else:
    LOGGER.error("Can't find score %s", f)
    return []

def read_score(score, commands):
  return ScoreReader(score, commands).read(load_score_elements(score.scorefile))
