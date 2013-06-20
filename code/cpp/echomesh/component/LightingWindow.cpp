#include "echomesh/component/LightingWindow.h"
#include "echomesh/network/SocketLineGetter.h"
#include "rec/util/thread/CallAsync.h"

namespace echomesh {

LightingWindow::LightingWindow()
  : DocumentWindow("echomesh lighting simulator",
                   Colours::lightgrey,
                   DocumentWindow::allButtons),
    instrumentGrid_(new echomesh::InstrumentGrid) {
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
}

void LightingWindow::closeButtonPressed() {
  if (SocketLineGetter* getter = SocketLineGetter::instance()) {
    YAML::Emitter out;

    out << YAML::BeginMap
        << YAML::Key << "type"
        << YAML::Value << "hide"
        << YAML::EndMap;

    getter->writeSocket(out.c_str(), out.size());
  }
}

void LightingWindow::moved() {
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

}  // namespace echomesh

