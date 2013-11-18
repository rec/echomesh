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
  std::cerr << "getReader!!\n";
  ScopedPointer<AudioFormatReader> reader(MANAGER->createReaderFor(File(name)));
  std::cerr << "reader created!! " << reader << "\n";
  if (end < 0)
    end = reader->lengthInSamples;
  if (begin or end < reader->lengthInSamples)
    reader = new AudioSubsectionReader(reader.release(), begin, end, true);
  std::cerr << "about to create afrs!!\n";
  auto afrs = new AudioFormatReaderSource(reader.release(), true);
  std::cerr << "returning reader!!\n";
  return afrs;
}

}  // namespace echomesh
