from __future__ import absolute_import, division, print_function, unicode_literals

import collections
import datetime
import threading
import weakref

from echomesh.base import CommandFile
from echomesh.base import Config
from echomesh.base import Yaml
from echomesh.element import Element
from echomesh.element import Score
from echomesh.util.thread import MasterRunnable
from echomesh.util import GetPrefix
from echomesh.util import Log
from echomesh.util import UniqueName

LOGGER = Log.logger(__name__)

def format_delta(t):
  s = str(datetime.timedelta(seconds=t))
  loc = s.find('.')
  if loc > 0:
    s = s[0:loc]
  return s

def format_score(score):
  if is_running:
    t = format_delta(time.time() - score.run_time)
  else:
    t = 'stopped'
  return '%-8s  %s' % (t, score.scorefile)

class ScoreMaster(MasterRunnable.MasterRunnable):
  STOP, START, UNLOAD = range(3)

  def __init__(self, *scores):
    super(ScoreMaster, self).__init__()
    self.elements = {}
    self.lock = threading.Lock()  # TODO: fill in locking
    self.scores_to_add = scores

  def load_scores(self, scores, names=None):
    if names is None:
      items = ((s, None) for s in scores)
    else:
      if len(names) > len(scores):
        LOGGER.warning('You have more names than scores.')
      items = itertools.izip_longest(scores, names)[:len(scores)]

    full_names = []
    for scorefile, name in items:
      scorefile = Yaml.filename(scorefile)
      elements = CommandFile.load('score', scorefile)

      description = {'elements': elements, 'type': 'score'}
      element = Score.Score(None, description, scorefile)

      with self.lock:
        if not name:
          name = scorefile[:-4]  # Remove .yaml.
        self._clean()
        name = UniqueName.unique_name(name, self.elements)
        self.elements[name] = element
        full_names.append(name)

      element.name = name
    return full_names

  def run_scores(self, scores, names=None):
    self.start_elements(self.load_scores(scores, names))

  def start_elements(self, names):
    return self._for_each_element(names, ScoreMaster.START)

  def stop_elements(self, names):
    return self._for_each_element(names, ScoreMaster.STOP)

  def unload_elements(self, names):
    return self._for_each_element(names, ScoreMaster.UNLOAD)

  def handle(self, event):
    for score, t in self.elements.itervalues():
      score.handle(event)

  def info(self):
    with self.lock:
      self._clean()
      return dict((k, format_score(s)) for k, s in self.elements.iteritems())

  def get_score(self, name):
    with self.lock:
      score = self.elements.get(name)
      if score:
        return score

      for k, v in self.elements.iteritems():
        if k.startswith(name):
          return v

  def _for_each_element(self, names, action):
    with self.lock:
      if '*' in names:
        names = self.elements.keys()
      full_names = []
      for name in names:
        try:
          full_name, element = GetPrefix.get_prefix_and_match(self.elements, name)
        except Exception as e:
          LOGGER.print_error('%s', str(e))
        else:
          full_names.append(full_name)

          if action == ScoreMaster.START:
            if element.is_running:
              LOGGER.print_error('Element %s was already running.', full_name)
            else:
              element.start()
          else:
            if element.is_running:
              element.stop()
            elif action == ScoreMaster.STOP:
              LOGGER.print_error('Element %s was not running.', name)

            if action == ScoreMaster.UNLOAD:
              del self.elements[full_name]

    return full_names

  def _on_start(self):
    try:
      self.load_scores(self.scores_to_add)
    except Exception as e:
      LOGGER.error(str(e))
    self.scores_to_add = ()

  def _clean(self):
    remove = [k for (k, v) in self.elements.iteritems() if not v[0].is_running]
    self.remove_slave(*remove)
    self.elements = dict((k, v) for (k, v) in self.elements.iteritems()
                       if v[0].is_running)

