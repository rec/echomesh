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
  instrumentGrid_->setConfig(config);
  rec::util::thread::callAsync(this, &LightingWindow::toFront, true);
}

void LightingWindow::toFront(bool foreground) {
  log(String("toFront") + (foreground ? " true" : " false"));
  setVisible(true);
  Thread::sleep(100);  // Values up to 2000 made no difference.
  Component::toFront(foreground);
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

}  // namespace echomesh

