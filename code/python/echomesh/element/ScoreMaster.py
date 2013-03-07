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
from echomesh.base import Yaml
from echomesh.element import Element
from echomesh.element import Root
from echomesh.util.thread import MasterRunnable
from echomesh.base import GetPrefix
from echomesh.util import Log
from echomesh.util import Split
from echomesh.util import UniqueName

LOGGER = Log.logger(__name__)
_NEW_STYLE_CALLS = True

class ScoreMaster(MasterRunnable.MasterRunnable):
  PAUSE, START, UNLOAD, RESET = range(4)

  def __init__(self):
    super(ScoreMaster, self).__init__()
    self.elements = {}
    self.lock = threading.Lock()  # TODO: put this in everywhere.
    self.scores_to_start = Split.split_scores(Config.get('score'))
    self.scores_to_load = Split.split_scores(Config.get('load_score'))

  def perform(self, action, names):
    if action == 'load':
      return self.load_elements(names)

    if action == 'start':
      return self.start_elements(names)

    if isinstance(names, six.string_types):
      names = Split.split_words(names)

    return self.perform_element(action, names)

  def perform_element(self, action, names):
    full_names = []
    getter = operator.attrgetter(action)
    is_unload = (action == 'unload')
    with self.lock:
      if '*' in names:
        names = self.elements.keys()
      for name in names:
        try:
          pm = GetPrefix.get_prefix_and_match(self.elements, name, 'element')
          full_name, element = pm
          if is_unload:
            if element.is_running:
              element.pause()
            del self.elements[full_name]
          else:
            getter(element)()
          full_names.append(full_name)
        except Exception:
          LOGGER.error()
    return full_names

  def load_elements(self, names):
    score_names = Split.split_scores(names)
    with self.lock:
      elements = _make_elements(score_names, self.elements)
      self.elements.update(elements)
      return elements.keys()

  def start_elements(self, names):
    element_names = []
    score_names = Split.split_scores(names)
    for score_file, name in score_names:
      is_file = score_file.endswith('.yml')
      if name:
        is_file = True
        score_file = Yaml.file(score_file)
      else:
        name = score_file
      if is_file:
        element_names.extend(self.load_elements([score_file, 'as', name]))
      else:
        element_names.append(name)

    return self.perform_element('run', element_names)

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

  def _on_run(self):
    super(ScoreMaster, self)._on_run()
    if self.scores_to_start or self.scores_to_load:
      for function, scores in ((self.start_elements, self.scores_to_start),
                               (self.load_elements, self.scores_to_load)):
        try:
          function(scores)
        except Exception as e:
          LOGGER.error()
        scores[:] = []

  def _on_pause(self):
    super(ScoreMaster, self)._on_pause()
    try:
      self.pause_elements('*')
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
