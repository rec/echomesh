#include <stdio.h>
#include <fstream>
#include <iostream>
#include <string>

#include "echomesh/network/MidiController.h"
#include "echomesh/network/SocketLineGetter.h"
#include "echomesh/util/GetDevice.h"

namespace echomesh {

using namespace std;

MidiController::MidiController(YAML::Node* node)
  : node_(node),
    midiInput_(new ConfigMidiInput(this)),
    midiOutput_(new ConfigMidiOutput) {
}

MidiController::~MidiController() {}

void MidiController::handleIncomingMidiMessage(MidiInput*, const MidiMessage& msg) {
  log("Incoming MIDI message");
  if (SocketLineGetter* getter = SocketLineGetter::instance()) {
    YAML::Emitter out;

    out << YAML::BeginMap
        << YAML::Key << "type"
        << YAML::Value << "midi"
        << YAML::Key << "data"
        << YAML::Value << YAML::BeginSeq;

    int size = msg.getRawDataSize();
    const uint8* data = msg.getRawData();
    for (int i = 0; i < size; ++i)
      out << static_cast<int>(data[i]);

    out << YAML::EndSeq << YAML::EndMap;

    getter->writeSocket(out.c_str(), out.size());
  }
}

static MidiMessage makeMidiMessage(const YAML::Node& data) {
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
  midiOutput_->sendMessageNow(makeMidiMessage((*node_)["data"]));
}

void MidiController::config() {
  Config config;
  (*node_)["data"] >> config;
  midiInput_->setConfig(config.midi.input);
  midiOutput_->setConfig(config.midi.output);
}

}  // namespace echomesh
