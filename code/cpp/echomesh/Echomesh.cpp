#include "echomesh/Echomesh.h"

#include "echomesh/audio/Player.h"
#include "echomesh/component/LightingWindow.h"
#include "echomesh/network/LightReader.h"

namespace echomesh {

struct Echomesh::Impl {
  LightingWindow lightingWindow_;
  LightReader lightReader_;
  Player player_;

  void initialize() {
    log("Starting echomesh.");
    player_.initialize();
    lightReader_.initialize(&lightingWindow_, player_.source());
  }

  void shutdown() {
    close_log();
  }
};

Echomesh::Echomesh() {
  impl_ = new Impl;
}

Echomesh::~Echomesh() {}

void Echomesh::initialise() {
  impl_->initialize();
}

void Echomesh::shutdown() {
  impl_->shutdown();
}

}  // namespace echomesh
