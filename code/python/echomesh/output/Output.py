from __future__ import absolute_import, division, print_function, unicode_literals

import itertools

from echomesh.output import make_output
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class Output(object):
  def __init__(self):
    self.parts = []

  def start(self):
    pass

  def pause(self):
    LOGGER.info('OUTPUT pause! %s', self.__class__)
    pass

  def finish_construction(self, description, is_redirect=True):
    self.clients = []
    if is_redirect:
      output = description.pop('output', None)
      if output is None:
        raise Exception('No output in %s' % self.__class__.__name__)
      if not isinstance(output, (list, tuple)):
        output = [output]

      self.output = [make_output(o) for o in output]
    else:
      self.output = []

    if description:
      LOGGER.error('Unknown keywords %s in output %s', description,
                   self.__class__.__name__)

  def add_client(self, client):
    if client in self.clients:
      LOGGER.error('Output', self, 'already contains client', client)
    else:
      self.clients.append(client)

  def remove_client(self, client):
    try:
      self.clients.remove(client)
    except ValueError:
      LOGGER.error('Output', self, 'did not contain client', client)

  def evaluate(self):
    bad_clients = []
    def _eval(c):
      try:
        return c.evaluate()
      except Exception as e:
        LOGGER.error('Got error from client %s, disabling', c)
        bad_clients.append(c)
    result = list(itertools.chain.from_iterable([_eval(c) for c in self.clients]))
    for c in bad_clients:
      self.remove_client(c)
    return result

  def clear(self):
    for o in self.output:
      o.clear()

  def emit_output(self, data):
    for o in self.output:
      o.emit_output(data)
