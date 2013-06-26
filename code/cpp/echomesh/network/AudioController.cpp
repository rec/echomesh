#include <stdio.h>
#include <fstream>
#include <iostream>
#include <string>

#include "echomesh/network/AudioController.h"
#include "echomesh/network/SocketLineGetter.h"
#include "echomesh/util/GetDevice.h"

namespace echomesh {

using namespace std;

AudioController::AudioController(YAML::Node* node) : node_(node) {}
AudioController::~AudioController() {}
void AudioController::audio() {
  log("audio");
}


}  // namespace echomesh
