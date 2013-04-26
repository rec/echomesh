#include "rec/util/STL.h"
#include "echomesh/component/InstrumentGrid.h"

namespace echomesh {

InstrumentGrid::InstrumentGrid() {
  setSize(64, 64);
}

InstrumentGrid::~InstrumentGrid() {
  rec::stl::deletePointers(&instruments_);
}

void InstrumentGrid::setConfig(const LightConfig& config) {
  MessageManagerLock l;
  config_ = config;
  int oldCount = instruments_.size();

  for (int i = config_.count; i < oldCount; ++i) {
    removeChildComponent(instruments_[i]);
    delete instruments_[i];
  }
  instruments_.resize(config_.count);
  for (int i = oldCount; i < config_.count; ++i) {
    instruments_[i] = new Instrument;
    addAndMakeVisible(instruments_[i]);
  }

  const LightDisplay& light = config_.display.light;
  int delta = light.labelStartsAtZero ? 0 : 1;
  for (int i = 0; i < instruments_.size(); ++i)
    instruments_[i]->configure(String(i + delta), light);

  int top = config_.display.padding.top;
  int left = config_.display.padding.left;
  int columns = config.display.layout.x;
  int rows = config.display.layout.y;

  int w = light.size.x + light.padding.x;
  int h = light.size.y + light.padding.y;
  int index = 0;
  for (int y = 0; y < rows; ++y) {
    for (int x = 0; x < columns; ++x) {
      instruments_[index++]->setBounds(left + x * w, top + y * h,
                                       light.size.x, light.size.y);
    }
  }

  setSize(left + w * columns + config_.display.padding.right,
          top + h * rows + config_.display.padding.bottom);
  repaint();
}

void InstrumentGrid::setLights(const ColorList& lights) {
  for (int i = 0; i < lights.size(); ++i)
    instruments_[i]->setColor(lights[i]);
}

void InstrumentGrid::paint(Graphics& g) {
  g.fillAll(config_.display.background);
}

}  // namespace echomesh

