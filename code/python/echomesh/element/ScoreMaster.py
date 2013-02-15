from __future__ import absolute_import, division, print_function, unicode_literals

import time
import threading
import weakref

from compatibility.collections import OrderedDict

from echomesh.base import CommandFile
from echomesh.base import Config
from echomesh.base import Yaml
from echomesh.element import Element
from echomesh.element import Score
from echomesh.util.thread import MasterRunnable
from echomesh.util import Log
from echomesh.util import UniqueName

LOGGER = Log.logger(__name__)

_SCORE = 'score/'

class ScoreMaster(MasterRunnable.MasterRunnable):
  def __init__(self):
    super(ScoreMaster, self).__init__()
    self.scores = OrderedDict()
    self.lock = threading.RLock()

  def start_score(self, scorefile):
    scorefile = Yaml.filename(scorefile)
    elements, error = CommandFile.load('element', scorefile)
    if error:
      LOGGER.error('%s: %s', scorefile, error)
      return

    description = {'elements': elements, 'type': 'score'}
    score = Score.Score(None, description)
    if scorefile.startswith(_SCORE):
      name = scorefile[len(_SCORE):]
    else:
      name = scorefile
    with self.lock:
      self._clean()
      name = UniqueName.unique_name(name, self.scores)
      self.scores[name] = score, time.strftime('%H:%M:%S')

    score.name = name
    score.start()
    self.add_slave(score)
    return score

  def _clean(self):
    remove = [k for (k, v) in self.scores.iteritems() if not v[0].is_running]
    self.remove_slave(*remove)
    self.scores = dict((k, v) for (k, v) in self.scores.iteritems()
                       if v[0].is_running)

  def info(self):
    with self.lock:
      self._clean()
      return dict((k, v[1]) for k, v in self.scores.iteritems())

  def get_score(self, name):
    with self.lock:
      score = self.scores.get(name)
      if score:
        return score

      for k, v in self.scores.iteritems():
        if k.startswith(name):
          return v
