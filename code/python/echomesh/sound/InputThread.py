from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Config
from echomesh.sound import GetFormatName
from echomesh.sound import Sound
from echomesh.sound.Input import Input
from echomesh.util import Log
from echomesh.util.thread.ThreadLoop import ThreadLoop

LOGGER = Log.logger(__name__)

MIN_CHUNK_SIZE = 16
MAX_CHUNK_SIZE = 2048

class InputThread(ThreadLoop):
  def __init__(self, device_index, sample_bytes, rates):
    super(InputThread, self).__init__(name='InputThread')
    self.chunk_size = max(MIN_CHUNK_SIZE,
                          min(MAX_CHUNK_SIZE,
                              Config.get('audio', 'input', 'chunk_size')))

    self.input = Input()
    fmt = GetFormatName.get_format_name(sample_bytes)
    try:
      len(rates)
    except TypeError:
      rates = [rates]

    self.clients = set()
    pyaud = Sound.PYAUDIO()
    for rate in rates:
      try:
        self.stream = pyaud.open(format=fmt, channels=1, rate=rate,
                                 input_device_index=device_index, input=True)
        break
      except IOError as e:
        if 'Invalid sample rate' not in str(e):
          raise
    else:
      raise Exception("Couldn't open audio device named %s." % device_index)

  def single_loop(self):
    try:
      self.input.receive(self.stream.read(self.chunk_size))
    except:
      LOGGER.error()
    else:
      for client in self.clients:
        client(self.input)

  def add_client(self, client):
    self.clients.add(client)

  def remove_client(self, client):
    self.clients.remove(client)

  def _after_thread_pause(self):
    self.stream.close()
    self.stream = None
