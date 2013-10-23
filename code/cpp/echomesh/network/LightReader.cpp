#include <stdio.h>
#include <fstream>
#include <iostream>
#include <string>

#include "base64/base64.h"
#include "echomesh/audio/AudioController.h"
#include "echomesh/audio/MidiController.h"
#include "echomesh/component/LightingWindow.h"
#include "echomesh/network/LightController.h"
#include "echomesh/network/LightReader.h"
#include "echomesh/util/Quit.h"
#include "rec/util/thread/FunctionCallback.h"
#include "rec/util/thread/MakeCallback.h"

namespace echomesh {

using namespace std;
using namespace rec::util::thread;

static const string DEFAULT_CONFIG =
  "data:\n"
  "  light:\n"
  "    brightness: 1.0\n"
  "    count: 256\n"
  "    enable: false\n"
  "    hardware: {enable: true, local: true, period: 0.005, rgb_order: rgb}\n"
  "    visualizer:\n"
  "      background: [1.0, 1.0, 1.0]\n"
  "      enable: true\n"
  "      instrument:\n"
  "        background: [0.3764705882352941, 0.3764705882352941, 0.3764705882352941]\n"
  "        border:\n"
  "          color: [0.0, 0.0, 0.0]\n"
  "          width: 1\n"
  "        label: false\n"
  "        label_padding: [2, 2]\n"
  "        label_starts_at_zero: false\n"
  "        padding: [2, 2]\n"
  "        paint_unclipped: false\n"
  "        shape: circle\n"
  "        size: [4, 4]\n"
  "      layout: [16, 16]\n"
  "      padding: [3, 3]\n"
  "      period: 0.010\n"
  "      show: true\n"
  "      top_left: [0, 44]\n"
  "      type: client\n"
  "      visualizer_closes_echomesh: true\n"
  "  midi:\n"
  "    input: {external: true, index: -1, name: from Max}\n"
  "    output: {external: true, index: -1, name: to Max}\n"
  "type: config\n"
  "---\n"
;

LightReader::LightReader(LightingWindow* wind, const String& commandLine,
                         PlaybackAudioSource* source)
    : ReadThread(commandLine),
      audioController_(new AudioController(node_, source)),
      lightController_(new LightController(wind, &node_)),
      midiController_(new MidiController(&node_)),
      lightingWindow_(wind),
      commandLine_(commandLine) {
}

void LightReader::initialize() {
  addHandler("audio", methodCallback(audioController_.get(),
                                     &AudioController::audio));
  addHandler("clear", methodCallback(lightController_.get(),
                                     &LightController::clear));
  addHandler("config", methodCallback(this, &LightReader::config));
  addHandler("light", methodCallback(lightController_.get(),
                                     &LightController::light));
  addHandler("midi", methodCallback(midiController_.get(),
                                    &MidiController::midi));
  addHandler("quit", functionCB(::echomesh::quit));

  if (commandLine_.isEmpty()) {
    lightingWindow_->setRunningInTest();
    parse(DEFAULT_CONFIG);
  }
}

LightReader::~LightReader() {
#if 0 && JUCE_LINUX
  fclose(file_);
#endif
}

void LightReader::config() {
  log("The client got the config message, and is configuring its parts.");
  lightController_->config();
  midiController_->config();
  log("The client finished configuring itself.");
}

}  // namespace echomesh
