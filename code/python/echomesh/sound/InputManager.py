from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util.thread import Lock

class InputManager(object):
  def __init__(self):
    self.thread = None
    self.lock = Lock.Lock()
    self.inputs = {}

  def add_client(self, client, device_name=None, device_index=None,
                 sample_bytes=None, rates=None):
    from echomesh.base import Config
    from echomesh.sound import Sound
    if device_index is None:
      if device_name is None:
        device_index = Sound.get_index_from_config(Sound.INPUT)
      else:
        device_index = Sound.get_index(device_name, device_index)
    sample_bytes = sample_bytes or Config.get('audio', 'input', 'sample_bytes')
    rates = rates or Config.get('audio', 'input', 'sample_rates')
    key = device_index, sample_bytes
    with self.lock:
      input = self.inputs.get(key, None)
      if input:
        input.clients.add(client)
      else:
        from echomesh.sound.InputThread import InputThread
        input_thread = InputThread(device_index, sample_bytes, rates)
        input_thread.add_client(client)
        self.inputs[key] = input_thread
        input_thread.run()

  def remove_client(self, client, key):
    with self.lock:
      thread = self.input[key]
      thread.clients.remove(client)
      if not thread.clients():
        input.pause()
        del self.input[key]

  def clear(self):
    with self.lock:
      for client in self.inputs.itervalues():
        client.pause()
      self.inputs.clear()

INPUT_MANAGER = InputManager()
