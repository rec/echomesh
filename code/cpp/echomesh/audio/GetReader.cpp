#include "echomesh/audio/GetReader.h"
#include "echomesh/audio/ResamplingPositionableAudioSource.h"

namespace echomesh {
namespace audio {

namespace {

AudioFormatManager* makeManager() {
  AudioFormatManager* manager = new AudioFormatManager();
  manager->registerBasicFormats();
  return manager;
}

unique_ptr<AudioFormatManager> MANAGER(makeManager());

}  // namespace

unique_ptr<PositionableAudioSource> getReader(
    const String& name, SampleTime begin, SampleTime end, float sampleRate,
    int channels) {
  unique_ptr<AudioFormatReader> reader(MANAGER->createReaderFor(File(name)));

  if (not reader.get()) {
    DLOG(ERROR) << "Can't read file " << name.toStdString();
    return nullptr;
  }

  if (end < 0)
    end = reader->lengthInSamples;

  if (begin or end < reader->lengthInSamples)
    reader.reset(new AudioSubsectionReader(reader.release(), begin, end, true));

  float inputSampleRate = reader->sampleRate;
  unique_ptr<PositionableAudioSource> source(
      new AudioFormatReaderSource(reader.release(), true));
  source->setLooping(true);

  if (static_cast<int>(sampleRate) != static_cast<int>(inputSampleRate)) {
    double ratio = inputSampleRate / sampleRate;
    source.reset(new ResamplingPositionableAudioSource(
        source.release(), true, ratio, channels));
  }
  return source;
}

}  // namespace audio
}  // namespace echomesh
