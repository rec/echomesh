#include <stdio.h>
#include <fstream>
#include <iostream>
#include <string>

#include "echomesh/audio/MidiController.h"
#include "echomesh/util/GetDevice.h"

namespace echomesh {
namespace audio {

using namespace std;

MidiController::MidiController(const Node& node)
  : node_(node),
    midiInput_(new ConfigMidiInput(this)),
    midiOutput_(new ConfigMidiOutput) {
}

MidiController::~MidiController() {}

void MidiController::handleIncomingMidiMessage(MidiInput*, const MidiMessage& msg) {
  log("Incoming MIDI message");
#if 0
    out << YAML::BeginMap
        << YAML::Key << "type"
        << YAML::Value << "midi"
        << YAML::Key << "data"
        << YAML::Value << YAML::BeginSeq;

    int size = msg.getRawDataSize();
    const uint8* data = msg.getRawData();
    for (int i = 0; i < size; ++i)
      out << static_cast<int>(data[i]);
#endif
}

static MidiMessage makeMidiMessage(const Node& data) {
  int size = data.size();
  int b;
  vector<uint8> bytes(size);
  for (int i = 0; i < size; ++i) {
    data[i] >> b;
    bytes[i] = static_cast<uint8>(b);
  }
  return MidiMessage(&bytes[0], size);
}

void MidiController::midi() {
  midiOutput_->sendMessageNow(makeMidiMessage(node_["data"]));
}

void MidiController::config() {
  Config config;
  node_["data"] >> config;
  midiInput_->setConfig(config.midi.input);
  midiOutput_->setConfig(config.midi.output);
}

}  // namespace audio
}  // namespace echomesh
