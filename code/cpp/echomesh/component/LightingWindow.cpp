#include "echomesh/component/LightingWindow.h"
#include "echomesh/network/SocketLineGetter.h"

namespace echomesh {

LightingWindow::LightingWindow()
  : DocumentWindow("echomesh lighting simulator",
                   Colours::lightgrey,
                   DocumentWindow::allButtons),
    instrumentGrid_(new echomesh::InstrumentGrid) {
  setContentOwned(instrumentGrid_, true);
  centreWithSize(getWidth(), getHeight());
  setVisible(true);
  setUsingNativeTitleBar(true);
}

void LightingWindow::setLights(const ColorList& cl) {
  instrumentGrid_->setLights(cl);
}

void LightingWindow::setConfig(const LightConfig& config) {
  instrumentGrid_->setConfig(config);
}

void LightingWindow::closeButtonPressed() {
  if (SocketLineGetter* getter = SocketLineGetter::instance()) {
    YAML::Emitter out;

    out << YAML::BeginMap
        << YAML::Key << "type"
        << YAML::Value << "close"
        << YAML::EndMap;

    getter->writeSocket(out.c_str(), out.size());
  }
}

}  // namespace echomesh

