from __future__ import absolute_import, division, print_function #, unicode_literals

import sndhdr

from echomesh.base import Config
from echomesh.sound import PlayerSetter
from echomesh.sound import Sound
from echomesh.sound import Util
from echomesh.util import ImportIf
from echomesh.util import Log
from echomesh.util.thread.ThreadLoop import ThreadLoop

numpy = ImportIf.imp('numpy')

LOGGER = Log.logger(__name__)

BITS_PER_BYTE = 8
MAX_DEVICE_NUMBERS = 8

UNKNOWN_FORMAT_ERROR = """\
%s
is not a file type that the pyaudio player can play.
Try using the client player, or the aplay player."""

INF = float('inf')

class FilePlayer(ThreadLoop):
  def __init__(self, element,
               level=1, pan=0, loops=1, begin=0.0, end=INF, **kwds):
    super(FilePlayer, self).__init__(name='FilePlayer')
    PlayerSetter.set_player(self, element,
                            level=1, pan=0, loops=1, begin=begin, end=end, **kwds)

    if begin > 0.0 or end != INF:
      LOGGER.error('The Python FilePlayer doesn\'t support begin or end')

    from echomesh.sound import SetOutput
    if not SetOutput.OUTPUT_SET:
      SetOutput.set_output()

    filename = Util.DEFAULT_AUDIO_DIRECTORY.expand(self._file)
    try:
      what = sndhdr.what(filename)
    except IOError:
      raise Exception('Can\'t open file %s' % filename)

    if not what:
      raise Exception(UNKNOWN_FORMAT_ERROR % filename)
    filetype = what[0]
    handler = Util.FILE_READERS.get(filetype)
    if not handler:
      LOGGER.error("Can't understand the file type of file %s", filename)
      self.pause()
      return

    self._file_stream = handler.open(filename, 'rb')
    self._sample_width = self._file_stream.getsampwidth()

    (self._channels, self._sample_width, self._sampling_rate,
     _, _, _) = self._file_stream.getparams()
    self._dtype = Util.numpy_types()[self._sample_width]
    self._request_channels = 2 if self._pan else self._channels
    self._format = Sound.PYAUDIO().get_format_from_width(self._sample_width)
    self._samples_per_frame = self._sample_width * self._channels
    self._loop_number = 0
    Config.add_client(self)
    self.restart_sound()

  def run(self):
    super(FilePlayer, self).run()

  def config_update(self, get):
    self._frames_per_buffer = get('audio', 'output', 'frames_per_buffer')
    self._chunk_size = get('audio', 'output', 'chunk_size')
    self._index = Sound.get_index_from_config(Sound.OUTPUT, get)

  def open_stream(self):
    try:
      return Sound.PYAUDIO().open(format=self._format,
                                  channels=self._request_channels,
                                  rate=self._sampling_rate,
                                  output=True,
                                  output_device_index=self._index,
                                  frames_per_buffer=self._frames_per_buffer)
    except:
      LOGGER.error('FAILED to open %s on port %s', self._file,
                   Sound.get_device_info(self._index)['name'])
    else:
      LOGGER.info('Opened %s on port %s', self._file,
                  Sound.get_device_info(self._index)['name'])

  def restart_sound(self):
    self._close_stream()
    self._audio_stream = self.open_stream()
    if not self._audio_stream:
      LOGGER.error("Couldn't open sound on loop %d", self._loop_number)
      self.pause()
    self._element.time = 0
    self._current_level = self._level()
    self._current_pan = self._pan()

  def _on_pause(self):
    super(FilePlayer, self)._on_pause()
    self._close_stream()

  def _close_stream(self):
    if getattr(self, 'audio_stream', None):
      self._audio_stream.stop_stream()
      self._audio_stream.close()

  def _convert(self, frames):
    frames = numpy.fromstring(frames, dtype=self._dtype)
    if self._sample_width == 1:
      frames *= 256.0
    elif self._sample_width == 4:
      frames /= 65536.0

    if self._channels == 1:
      return numpy.vstack((frames, numpy.array(frames)))
    else:
      return Util.uninterleave(frames)

  def single_loop(self):
    if not self._audio_stream:
      LOGGER.error('FilePlayer.single_loop terminates')
      # TODO: why should I have to do this given that restart_sound calls pause?
      self.pause()
      return

    frames = self._file_stream.readframes(self._chunk_size)
    if not frames:
      self._loop_number += 1
      if self._loop_number < self._loops:
        self.restart_sound()
        if not self.is_running:
          return
      else:
        self.pause()
        return

    # TODO: below I had written =+ instead of +=!  Does anything change?
    self._element.time += len(frames) / float((self._samples_per_frame *
                                              self._sampling_rate))

    frames = self._pan_and_fade(frames)
    try:
      self._audio_stream.write(frames)
    except:
      if self.is_running:
        raise

  def _pan_and_fade(self, frames):
    if self._passthrough:
      return frames

    left, right = Util.to_numpy(frames, self._dtype,
                                self._sample_width, self._channels)
    if self._level.is_constant():
      left *= self._current_level
      right *= self._current_level
    else:
      next_level = self._level()
      levels = numpy.linspace(self._current_level, next_level, len(left))
      left *= levels
      right *= levels
      self._current_level = next_level

    if self._pan.is_constant():
      lpan, rpan = Util.calculate_pan(self._current_pan)
      left *= lpan
      right *= rpan
    else:
      next_pan = self._pan()
      angles = numpy.linspace(Util.pan_to_angle(self._current_pan),
                              Util.pan_to_angle(next_pan), len(left))

      left *= numpy.cos(angles)
      right *= numpy.sin(angles)
      self._current_pan = next_pan

    return Util.interleave(left, right).tostring()
