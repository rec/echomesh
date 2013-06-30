#include "echomesh/audio/GetReader.h"

namespace echomesh {

namespace {

AudioFormatManager* makeManager() {
  AudioFormatManager* manager = new AudioFormatManager();
  manager->registerBasicFormats();
  return manager;
}

ScopedPointer<AudioFormatManager> MANAGER(makeManager());

}  // namespace

PositionableAudioSource* getReader(const String& name,
                                   SampleTime begin, SampleTime end) {
  ScopedPointer<AudioFormatReader> reader(MANAGER->createReaderFor(File(name)));
  if (begin or end < reader->lengthInSamples)
    reader = new AudioSubsectionReader(reader.release(), begin, end, true);
  return new AudioFormatReaderSource(reader.release(), true);
}

}  // namespace echomesh
