#include "echomesh/component/LightingWindow.h"
#include "echomesh/network/SocketLineGetter.h"
#include "echomesh/util/Quit.h"
#include "rec/util/thread/CallAsync.h"

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

void LightingWindow::closeButtonPressed() {
  if (runningInTest_) {
    quit();

  } else if (SocketLineGetter* getter = SocketLineGetter::instance()) {
    YAML::Emitter out;

    out << YAML::BeginMap
        << YAML::Key << "type"
        << YAML::Value << "hide"
        << YAML::EndMap;

    getter->writeSocket(out.c_str(), out.size());
  }
}

void LightingWindow::moved() {
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
}

LightingWindow* makeLightingWindow() {
  unique_ptr<LightingWindow> window = make_unique<LightingWindow>();
  MessageManagerLock l;

  window->toFront(true);
  window->setVisible(true);
  DLOG(INFO) << "Finished initializing the lighting window.";
  return window.release();
}

}  // namespace echomesh

