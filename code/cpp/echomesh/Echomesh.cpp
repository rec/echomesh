#include "echomesh/Echomesh.h"

#include "echomesh/audio/Player.h"
#include "echomesh/component/LightingWindow.h"
#include "echomesh/network/LightReader.h"

namespace echomesh {

Echomesh::~Echomesh() {}

void Echomesh::initialise() {
  player_ = new Player;
  player_->initialize();
  lightingWindow_ = new LightingWindow;

  readThread_ = new LightReader(lightingWindow_, "", player_->source());
  readThread_->initialize();
  readThread_->startThread();
}

void Echomesh::shutdown() {
  lightingWindow_ = nullptr;
  close_log();
}

}  // namespace echomesh
