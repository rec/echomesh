from __future__ import absolute_import, division, print_function, unicode_literals

import collections
import itertools
import operator
import os.path
import six
import threading
import weakref

from echomesh.base import CommandFile
from echomesh.base import Config
from echomesh.base import Split
from echomesh.base import Yaml
from echomesh.element import Element
from echomesh.element import Root
from echomesh.util.thread import MasterRunnable
from echomesh.util import GetPrefix
from echomesh.util import Log
from echomesh.util import UniqueName

LOGGER = Log.logger(__name__)

class ScoreMaster(MasterRunnable.MasterRunnable):
  STOP, START, UNLOAD, RESET = range(4)

  def __init__(self):
    super(ScoreMaster, self).__init__()
    self.elements = {}
    self.lock = threading.Lock()
    self.scores_to_start = Split.split_scores(Config.get('score'))
    self.scores_to_load = Split.split_scores(Config.get('load_score'))

  def load_elements(self, score_names):
    with self.lock:
      elements = _make_elements(score_names, self.elements)
      self.elements.update(elements)
      return elements.keys()

  def perform(self, method_name, score_names):
    full_names = []
    getter = operator.attrgetter(method_name)
    is_unload = (method_name == unload)
    with self.lock:
      if '*' in names:
        names = self.elements.keys()
      for name in names:
        try:
          pm = GetPrefix.get_prefix_and_match(self.elements, name, 'element')
          full_name, element = pm
          attr = getattr(element, method_name)
          getter(element)()
          full_names.append(full_name)
          if is_unload:
            del self.elements[full_name]
        except Exception:
          LOGGER.error()
    return full_names

  def run_elements(self, score_names):
    element_names = []
    for score_file, name in score_names:
      is_file = score_file.endswith('.yml')
      if name:
        is_file = True
        score_file = Yaml.file(score_file)
      else:
        name = score_file
      if is_file:
        element_names.extend(self.load_elements([[score_file, name]]))
      else:
        element_names.append(name)
    return self.start_elements(element_names)

  def start_elements(self, elements):
    return self._for_each_element(elements, ScoreMaster.START)

  def stop_elements(self, elements):
    return self._for_each_element(elements, ScoreMaster.STOP)

  def unload_elements(self, names):
    return self._for_each_element(names, ScoreMaster.UNLOAD)

  def reset_elements(self, names):
    return self._for_each_element(names, ScoreMaster.RESET)

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
        assert name is not None
        try:
          full_names.append(self._for_one_element(name, action))
        except Exception:
          LOGGER.error()
    return full_names

  def _for_one_element(self, name, action):
    full_name, element = GetPrefix.get_prefix_and_match(
      self.elements, name, 'element')

    if action == ScoreMaster.START:
      if element.is_running:
        raise Exception('Element %s was already running.' % full_name)
      element.run()

    elif action == ScoreMaster.RESET:
      element.reset()

    else:
      if element.is_running:
        element.stop()
      elif action == ScoreMaster.STOP:
        raise Exception('Element %s was not running.' % full_name)

      if action == ScoreMaster.UNLOAD:
        del self.elements[full_name]

    return full_name

  def _on_run(self):
    super(ScoreMaster, self)._on_run()
    for function, scores in ((self.start_elements, self.scores_to_start),
                             (self.load_elements, self.scores_to_load)):
      try:
        function(scores)
      except Exception as e:
        LOGGER.error()
      scores[:] = []

  def _on_stop(self):
    super(ScoreMaster, self)._on_stop()
    try:
      self.stop_elements('*')
    except:
      pass


def _make_elements(score_names, table):
  result = {}
  for score_file, name in score_names:
    resolved_file = CommandFile.resolve('score', Yaml.filename(score_file))
    elements = Yaml.read(resolved_file)
    description = {'element': elements, 'type': 'score'}
    parts = resolved_file.split('/')
    final_file = '/'.join([parts[1]] + parts[3:])

    try:
      element = Root.Root(description, final_file)
    except Exception as e:
      LOGGER.error("Couldn't read score file %s", score_file)
      continue

    name = os.path.splitext(name or score_file)[0]
    name = UniqueName.unique_name(name, table)
    result[name] = element
    element.name = name

  return result
