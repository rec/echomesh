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

PositionableAudioSource* getReader(const String& name) {
  return new AudioFormatReaderSource(MANAGER->createReaderFor(File(name)), true);
}

}  // namespace echomesh
