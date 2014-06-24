from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.Cechomesh import cechomesh

from echomesh.base import Config

def input_level_maker():
  return cechomesh.AudioLoudness(
    name=Config.get('audio', 'input', 'device_name'),
    channels=Config.get('audio', 'input', 'channels'),
    chunk_size=Config.get('audio', 'input', 'chunk_size'),
    sample_rate=Config.get('audio', 'input', 'sample_rate')).loudness
