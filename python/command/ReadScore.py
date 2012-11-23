from __future__ import absolute_import, division, print_function, unicode_literals

from util.DefaultFile import DefaultFile
from util import File
from util import Log

LOGGER = Log.logger(__name__)

DEFAULT_SCORE_DIRECTORY = DefaultFile('score')
DEFAULT_ELEMENT_DIRECTORY = DefaultFile('element')
DEFAULT_SCORE = 'score.yml'
LOCAL_SCORE = 'local/echomesh-score.yml'

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
  elements = File.yaml_load_all(LOCAL_SCORE)
  if elements:
    scorefile = LOCAL_SCORE
  else:
    scorefile = DEFAULT_SCORE_DIRECTORY.expand(scorefile or DEFAULT_SCORE)

  elements = File.yaml_load_all(scorefile)
  LOGGER.info('Loading score %s', DEFAULT_SCORE_DIRECTORY.relpath(scorefile))
  return elements

def read_score(score, commands):
  return ScoreReader(score, commands).read(load_score_elements(score.scorefile))
