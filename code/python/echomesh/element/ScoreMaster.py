from __future__ import absolute_import, division, print_function, unicode_literals

import collections
import itertools
import os.path
import six
import threading
import weakref

from echomesh.base import CommandFile
from echomesh.base import Config
from echomesh.base import Yaml
from echomesh.element import Element
from echomesh.element import Root
from echomesh.util.thread import MasterRunnable
from echomesh.util import GetPrefix
from echomesh.util import Log
from echomesh.util import Split
from echomesh.util import UniqueName

LOGGER = Log.logger(__name__)

class ScoreMaster(MasterRunnable.MasterRunnable):
  STOP, START, UNLOAD = range(3)

  def __init__(self):
    super(ScoreMaster, self).__init__()
    self.elements = {}
    self.lock = threading.Lock()  # TODO: fill in locking
    self.scores_to_add = Split.split_scores(Config.get('score'))
    self.scores_to_load = Split.split_scores(Config.get('load_score'))

  def load_scores(self, scores, names=None):
    if not names:
      items = [(s, None) for s in scores]
    else:
      items = list(itertools.izip_longest(scores, names))
      if len(names) > len(scores):
        LOGGER.warning('You have more names than scores.')
        items = items[:len(scores)]

    full_names = []
    for score_file, name in items:
      resolved_file = CommandFile.resolve('score', Yaml.filename(score_file))
      elements = Yaml.read(resolved_file)
      description = {'elements': elements, 'type': 'score'}
      parts = resolved_file.split('/')
      final_file = '/'.join([parts[1]] + parts[3:])

      try:
        element = Root.Root(None, description, final_file)
      except Exception as e:
        LOGGER.print_error("Couldn't read score file %s", score_file)
        continue

      with self.lock:
        name = os.path.splitext(name or score_file)[0]
        name = UniqueName.unique_name(name, self.elements)
        self.elements[name] = element
        full_names.append(name)

      element.name = name
    return full_names

  def run_scores(self, scores, names=None):
    return self.start_elements(self.load_scores(scores, names))

  def start_elements(self, names):
    return self._for_each_element(names, ScoreMaster.START)

  def stop_elements(self, names):
    return self._for_each_element(names, ScoreMaster.STOP)

  def unload_elements(self, names):
    return self._for_each_element(names, ScoreMaster.UNLOAD)

  def handle(self, event):
    for score in self.elements.itervalues():
      score.handle(event)

  def info(self):
    with self.lock:
      return dict(self.elements)

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
          full_name, element = GetPrefix.get_prefix_and_match(
            self.elements, name, 'element')
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
      self.run_scores(*self.scores_to_add)
    except Exception as e:
      LOGGER.print_error(str(e))
    self.scores_to_add = ()

    try:
      self.load_scores(*self.scores_to_load)
    except Exception as e:
      LOGGER.print_error(str(e))
    self.scores_to_load = ()

  def _on_stop(self):
    try:
      self.stop_elements('*')
    except:
      pass

  def clean(self):
    remove, elements = [], {}
    for k, v in self.elements.iteritems():
      if v.is_running:
        elements[k] = v
      else:
        self.remove_slave(vi)
    self.elements = elements
