#include "rec/util/STL.h"
#include "echomesh/component/InstrumentGrid.h"

namespace echomesh {

static const int TOP_TWEAK = 5;
static const int LEFT_TWEAK = 5;

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
    instruments_[i] = new InstrumentComponent;
    addAndMakeVisible(instruments_[i]);
  }

  const Instrument& instrument = config_.visualizer.instrument;
  int delta = instrument.labelStartsAtZero ? 0 : 1;
  for (int i = 0; i < instruments_.size(); ++i) {
    InstrumentComponent* inst = instruments_[i];
    inst->setPaintingIsUnclipped(config_.visualizer.instrument.paintUnclipped);
    inst->configure(String(i + delta), instrument);
  }

  int top = config_.visualizer.padding.y;
  int left = config_.visualizer.padding.x;
  int columns = config_.visualizer.layout.x;
  int rows = config_.visualizer.layout.y;

  int w = instrument.size.x + instrument.padding.x;
  int h = instrument.size.y + instrument.padding.y;
  int index = 0;
  for (int y = 0; y < rows and index < instruments_.size(); ++y) {
    for (int x = 0; x < columns and index < instruments_.size(); ++x) {
      instruments_[index++]->setBounds(left + x * w, top + y * h,
                                       instrument.size.x, instrument.size.y);
    }
  }

  int screenWidth = left + w * columns + config_.visualizer.padding.x,
    screenHeight = top + h * rows + config_.visualizer.padding.y;

  log(String(screenWidth) + "x" + String(screenHeight));

  setSize(screenWidth, screenHeight);
  repaint();
}

void InstrumentGrid::setLights(const ColorList& lights) {
  MessageManagerLock l;
  for (int i = 0; i < lights.size(); ++i)
    instruments_[i]->setColor(lights[i]);
}

void InstrumentGrid::paint(Graphics& g) {
  g.fillAll(config_.visualizer.background);
}

}  // namespace echomesh

