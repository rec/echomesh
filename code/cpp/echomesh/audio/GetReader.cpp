#include "echomesh/audio/GetReader.h"

namespace echomesh {

namespace {

AudioFormatManager* makeManager() {
  AudioFormatManager* manager = new AudioFormatManager();
  manager->registerBasicFormats();
  return manager;
}

unique_ptr<AudioFormatManager> MANAGER(makeManager());

}  // namespace

PositionableAudioSource* getReader(const String& name,
                                   SampleTime begin, SampleTime end) {
  unique_ptr<AudioFormatReader> reader(MANAGER->createReaderFor(File(name)));

  if (not reader.get()) {
    LOG(ERROR) << "Can't read file " << name.toStdString();
    std::cerr <<  "Can't read file " << name.toStdString() << "\n";
    throw new Exception(("Can't read file " + name).toStdString());
    return nullptr;
  }
  if (end < 0)
    end = reader->lengthInSamples;
  if (begin or end < reader->lengthInSamples)
    reader.reset(new AudioSubsectionReader(
        reader.release(), begin, end, true));
  return new AudioFormatReaderSource(reader.release(), true);
}

}  // namespace echomesh
