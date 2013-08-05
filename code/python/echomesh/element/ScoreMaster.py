from __future__ import absolute_import, division, print_function, unicode_literals

import operator
import os.path
import six

from echomesh.base import CommandFile
from echomesh.base import Config
from echomesh.base import GetPrefix
from echomesh.base import Yaml
from echomesh.element import Root
from echomesh.util import Log
from echomesh.util.string import Split
from echomesh.util.string import UniqueName
from echomesh.util.thread import MasterRunnable
from echomesh.util.thread import TkThreadRunner
from echomesh.util.thread import Lock

LOGGER = Log.logger(__name__)
_NEW_STYLE_CALLS = True

EMPTY_IMPLIES_EVERYTHING = set(['begin', 'pause', 'reload', 'run', 'start',
                                'unload'])

class ScoreMaster(MasterRunnable.MasterRunnable):
  INSTANCE = None

  def __init__(self):
    super(ScoreMaster, self).__init__()
    self.elements = {}
    self.lock = Lock.Lock()  # TODO: put this in everywhere.
    self.startup = True
    assert not ScoreMaster.INSTANCE
    ScoreMaster.INSTANCE = self

  def perform(self, action, names):
    if action == 'load':
      return self._load_elements(names)

    if action == 'start':
      return self.start_elements(names)

    if isinstance(names, six.string_types):
      names = Split.split_words(names)

    return self.perform_element(action, names)

  def get_prefix(self, name):
    return GetPrefix.get_prefix(self.elements, name)

  def perform_element(self, action, names):
    is_unload = (action == 'unload')
    is_reload = (action == 'reload')
    full_names = []
    assert isinstance(action, six.string_types), action
    getter = operator.attrgetter(action)
    with self.lock:
      if (((action in EMPTY_IMPLIES_EVERYTHING) and not names)
          or names and (names[0] == '*')):
        names = self.elements.keys()
      for name in names:
        try:
          full_name, element = self.get_prefix(name)
          if is_unload:
            element.unload()
            del self.elements[full_name]
          elif is_reload:
            self.elements[full_name] = element.clone()
            element.unload()
          else:
            getter(element)()
          full_names.append(full_name)
        except Exception as e:
          LOGGER.error('', exc_info=0)
    return full_names

  def start_elements(self, names):
    score_names = Split.split_scores(names)
    element_names = []
    for score_file, name in score_names:
      if name:
        is_file = True
      else:
        name = score_file
        is_file = Yaml.has_extension(score_file)
        if is_file:
          name = name[:-4]
        elif name not in self.elements:
          is_file = True
      if is_file:
        element_names.extend(self._load_raw_elements([[score_file, name]]))
      else:
        element_names.append(name)

    return self.perform_element('start', element_names)

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

      for k, v in six.iteritems(self.elements):
        if k.startswith(name):
          return v

  def _on_run(self):
    super(ScoreMaster, self)._on_run()
    if self.startup:
      self.startup = False
      try:
        self._load_elements(Config.get('load'))
      except:
        LOGGER.error()
      try:
        self.start_elements(Config.get('start'))
      except:
        LOGGER.error()

  def _on_pause(self):
    super(ScoreMaster, self)._on_pause()
    try:
      self.perform_element('pause', [])
    except:
      pass

  def _load_elements(self, names):
    return self._load_raw_elements(Split.split_scores(names))

  def _load_raw_elements(self, score_names):
    with self.lock:
      elements = _make_elements(score_names, self.elements)
      self.elements.update(elements)
      return elements.keys()

def _make_elements(score_names, table):
  result = {}
  for score_file, name in score_names:
    resolved_file = CommandFile.resolve('score', score_file)
    if not resolved_file:
      LOGGER.error('No such score file: "%s".',
                   CommandFile.base_file('score', score_file))
      continue
    elements = Yaml.read(resolved_file)
    description = {'elements': elements, 'type': 'score'}
    parts = resolved_file.split('/')
    final_file = '/'.join([parts[1]] + parts[3:])

    try:
      element = Root.Root(description, final_file)
    except Exception:
      LOGGER.error("\nError when reading score file %s", score_file, exc_info=1)
      continue

    name = os.path.splitext(name or score_file)[0]
    name = UniqueName.unique_name(name, table)
    result[name] = element
    element.name = name

  return result
