#include <stdio.h>
#include <fstream>
#include <iostream>
#include <string>

#include "yaml-cpp/yaml.h"

#include "echomesh/audio/AudioController.h"
#include "echomesh/audio/PlaybackAudioSource.h"
#include "echomesh/audio/SampleAudioSource.h"
#include "echomesh/network/SocketLineGetter.h"
#include "echomesh/util/GetDevice.h"
#include "rec/util/STL.h"

namespace echomesh {

using namespace std;

AudioController::AudioController(Node* node, PlaybackAudioSource* source)
    : node_(node), playbackSource_(source) {
}

AudioController::~AudioController() {
  rec::stl::deleteMapPointers(&sources_);
}

void AudioController::audio() {
  const Node& data = (*node_)["data"];
  string type;
  Hash hash;
  data["type"] >> type;
  data["hash"] >> hash;
  SampleAudioSource*& source = sources_[hash];

  log("Receiving " + type);
  if (type == "construct") {
    if (source) {
      log("Warning: already created a source for hash " + String(hash));
      return;
    }
    source = new SampleAudioSource(data);
    playbackSource_->addSource(source);
    return;
  }

  if (not source) {
    log("No source?? " + type);
  } else if (type == "run") {
    log("run");
    source->run();
  } else if (type == "begin") {
    log("begin");
    source->begin();
  } else if (type == "pause") {
    log("pause");
    source->pause();
  } else if (type == "unload") {
    playbackSource_->removeSource(source);
    sources_.erase(hash);
  }
}

}  // namespace echomesh
