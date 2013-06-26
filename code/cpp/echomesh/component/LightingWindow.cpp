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
    initialized_(false),
    runningInTest_(false) {
  setContentOwned(instrumentGrid_, true);
  centreWithSize(getWidth(), getHeight());
  setUsingNativeTitleBar(true);
}

void LightingWindow::setLights(const ColorList& cl) {
  instrumentGrid_->setLights(cl);
}

void LightingWindow::setConfig(const LightConfig& config) {
  MessageManagerLock l;
  setTopLeftPosition(config.visualizer.topLeft.x, config.visualizer.topLeft.y);
  instrumentGrid_->setConfig(config);
  toFront(true);
  initialized_ = true;
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
  if (initialized_) {
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

}  // namespace echomesh

