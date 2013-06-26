#include <stdio.h>
#include <fstream>
#include <iostream>
#include <string>

#include "yaml-cpp/yaml.h"

#include "echomesh/audio/AudioController.h"
#include "echomesh/audio/EnvelopeAudioSource.h"
#include "echomesh/network/SocketLineGetter.h"
#include "echomesh/util/GetDevice.h"
#include "rec/util/STL.h"

namespace echomesh {

using namespace std;

AudioController::AudioController(YAML::Node* node) : node_(node) {}

AudioController::~AudioController() {
  rec::stl::deleteMapPointers(&sources_);
}

void AudioController::audio() {
  const YAML::Node& data = (*node_)["data"];
  string type;
  Hash hash;
  data["type"] >> type;
  data["hash"] >> hash;
  EnvelopeAudioSource*& source = sources_[hash];

  if (type == "construct") {
    if (source)
      log("Warning: already created a source for hash " + String(hash));
    else
      source = new EnvelopeAudioSource(data);
  } else if (type == "run") {
    source->run();
  } else if (type == "begin") {
    source->begin();
  } else if (type == "pause") {
    source->pause();
  } else if (type == "unload") {
    source->unload();
  }
}

}  // namespace echomesh
