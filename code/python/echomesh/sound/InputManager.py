from __future__ import absolute_import, division, print_function, unicode_literals

class InputManager(object):
  def __init__(self):
    self.thread = None
    self.lock = threading.Lock()
    self.inputs = {}

  def add_client(self, client, device_index, sample_bytes, rates):
    key = device_index, sample_bytes
    with self.lock:
      input = self.inputs.get(key, None)
      if input:
        input.clients.add(client)
      else:
        from echomesh.audio.InputThread import InputThread
        input = InputThread(device_index, sample_bytes, rates)
        input.add_client(client)
        self.inputs[key] = input
        input.run()

  def remove_client(self, client, key):
    with self.lock:
      thread = self.input[key]
      thread.clients.remove(client)
      if not thread.clients():
        input.pause()
        del self.input[key]
