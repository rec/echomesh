from __future__ import absolute_import, division, print_function, unicode_literals

import itertools
from weakref import WeakSet

from echomesh.output.Registry import make_output
from echomesh.util import Log
from echomesh.util.thread.MasterRunnable import MasterRunnable

LOGGER = Log.logger(__name__)

class Output(MasterRunnable):
    OUTPUTS = WeakSet()

    def __init__(self):
        super(Output, self).__init__()
        self.parts = []
        Output.OUTPUTS.add(self)

    def finish_construction(self, description, is_redirect=True):
        self.clients = []
        if is_redirect:
            output = description.pop('output', None)
            if output is None:
                raise Exception('No output in %s' % self.__class__.__name__)
            if not isinstance(output, (list, tuple)):
                output = [output]

            self.output = [make_output(o) for o in output]
            if False:  # TODO
                for o in self.output:
                    o.add_client(self)
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
            LOGGER.error(
                'Output %s did not contain %s', self, client, exc_info=0)

    def evaluate(self):
        bad_clients = []
        result = []
        for c in self.clients:
            try:
                result.append(c.evaluate())
            except Exception as e:
                LOGGER.error(
                    'Got error from client %s, disabling output client', c)
                bad_clients.append(c)
        result = list(itertools.chain.from_iterable(result))
        for c in bad_clients:
            self.remove_client(c)
        return result

    def clear(self):
        for o in self.output:
            o.clear()

    def emit_output(self, data):
        for o in self.output:
            o.emit_output(data)


def pause_outputs():
    for o in Output.OUTPUTS:
        try:
            o.pause()
        except:
            pass
