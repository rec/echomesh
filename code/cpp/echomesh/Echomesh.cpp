#include "echomesh/Echomesh.h"

#include "echomesh/audio/Player.h"
#include "echomesh/component/LightingWindow.h"
#include "echomesh/network/LightReader.h"

namespace echomesh {

class KeyboardThread : public Thread {
 public:
  KeyboardThread() : Thread("keyboard") {}

  virtual void run() {
    std::cout << "Input data: ";
    std::cout.flush();
    string data;
    std::cin >> data;
    std::cout << "\ndata: " << data << "\n";
    std::cout.flush();
  }
};


struct Echomesh::Impl {
  LightingWindow lightingWindow_;
  LightReader lightReader_;
  audio::Player player_;
  ScopedPointer<Thread> thread_;

  void initialize() {
    log("Starting echomesh.");
    lightReader_.initialize(&lightingWindow_);
    player_.initialize(lightReader_.source());
    thread_ = new KeyboardThread;
    thread_->startThread();
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
