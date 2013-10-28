#include "echomesh/Echomesh.h"

#include "echomesh/audio/Player.h"
#include "echomesh/component/LightingWindow.h"
#include "echomesh/network/LightReader.h"

namespace echomesh {

struct Echomesh::Impl {
  ScopedPointer<LightingWindow> lightingWindow_;
  ScopedPointer<LightReader> readThread_;
  ScopedPointer<Player> player_;

  void initialize() {
    log("Starting echomesh.");

    player_ = new Player;
    player_->initialize();
    lightingWindow_ = new LightingWindow;

    readThread_ = new LightReader(lightingWindow_, player_->source());
    readThread_->initialize();
    readThread_->startThread();
  }

  void shutdown() {
    lightingWindow_ = nullptr;
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
