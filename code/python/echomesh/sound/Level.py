from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.Cechomesh import cechomesh

from echomesh.base import Settings

def input_level_maker():
    return cechomesh.AudioLoudness(
      name=Settings.get('audio', 'input', 'device_name'),
      channels=Settings.get('audio', 'input', 'channels'),
      chunk_size=Settings.get('audio', 'input', 'chunk_size'),
      sample_rate=Settings.get('audio', 'input', 'sample_rate')).loudness
