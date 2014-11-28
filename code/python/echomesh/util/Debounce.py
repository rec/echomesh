from __future__ import absolute_import, division, print_function, unicode_literals

DEFAULT_DEBOUNCE_COUNT = 2

class Client(object):
    def __init__(self, client):
        self.client = client
        self.state = None
        self.count = 0

    def update(self, debounce_count):
        state = self.client.state()
        if state == self.state:
            self.count += 1
        else:
            self.count = 1
            self.state = state

        if self.count == debounce_count:
            self.client.update(state)


class Debounce(object):
    def __init__(self, debounce_count=DEFAULT_DEBOUNCE_COUNT):
        self.clients = []
        self.debounce_count = debounce_count

    def add_client(self, client):
        c = Client(client)
        self.clients.append(c)
        return c

    def update(self):
        for c in self.clients:
            c.update(self.debounce_count)
