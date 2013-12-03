#include "echomesh/component/LightingWindow.h"
#include "echomesh/util/Quit.h"
#include "echomesh/util/RunOnMessageThread.h"

namespace echomesh {

LightingWindow::LightingWindow()
  : DocumentWindow("echomesh lighting simulator",
                   Colours::lightgrey,
                   DocumentWindow::allButtons),
    instrumentGrid_(new echomesh::InstrumentGrid),
    runningInTest_(false) {
  setContentOwned(instrumentGrid_, true);
  centreWithSize(getWidth(), getHeight());
  setUsingNativeTitleBar(true);
}

void LightingWindow::setConfig(const LightConfig& config) {
  MessageManagerLock l;
  setTopLeftPosition(config.visualizer.topLeft.x, config.visualizer.topLeft.y);
  instrumentGrid_->setConfig(config);
  toFront(true);
}

LightingWindow::~LightingWindow() {}

void LightingWindow::closeButtonPressed() {
  if (runningInTest_) {
    quit();

  } else {
#if 0
    out << YAML::BeginMap
        << YAML::Key << "type"
        << YAML::Value << "hide"
#endif
  }
}

void LightingWindow::moved() {
#if 0
  if (false) {
    if (SocketLineGetter* getter = SocketLineGetter::instance()) {
      YAML::Emitter out;

      out << YAML::BeginMap
          << YAML::Key << "type"
          << YAML::Value << "move"
          << YAML::Key << "top_left"
          << YAML::Value << YAML::BeginSeq
          << getX() << getY() - getTitleBarHeight()
          << YAML::EndSeq
          << YAML::EndMap;

      getter->writeSocket(out.c_str(), out.size());
    }
  }
#endif
}

LightingWindow* makeLightingWindow() {
  unique_ptr<LightingWindow> window = make_unique<LightingWindow>();
  MessageManagerLock l;

  window->toFront(true);
  window->setVisible(true);
  window->grid()->setLightCount(256);
  return window.release();
}

void deleteLightingWindow(LightingWindow* window) {
  runOnMessageThread(&LightingWindow::~LightingWindow, window);
}

}  // namespace echomesh
