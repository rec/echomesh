#include <stdio.h>
#include <fstream>
#include <iostream>
#include <string>

#include "echomesh/audio/MidiController.h"
#include "echomesh/util/GetDevice.h"

namespace echomesh {
namespace audio {

using namespace std;

MidiController::MidiController()
#if 0
        : midiInput_(new ConfigMidiInput(this)),
          midiOutput_(new ConfigMidiOutput)
#endif
{
}

MidiController::~MidiController() {}

void MidiController::handleIncomingMidiMessage(MidiInput*, const MidiMessage& msg) {
    DLOG(INFO) << ("Incoming MIDI message");
#if 0
    int size = msg.getRawDataSize();
    const uint8* data = msg.getRawData();
    for (int i = 0; i < size; ++i)
        out << static_cast<int>(data[i]);
#endif
}

#if 0
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

#endif

}  // namespace audio
}  // namespace echomesh
