#include "rec/util/STL.h"
#include "echomesh/base/Config.h"
#include "echomesh/component/InstrumentGrid.h"

namespace echomesh {

static const int TOP_TWEAK = 5;
static const int LEFT_TWEAK = 5;

InstrumentGrid::InstrumentGrid()
    : isUnclipped_(false), labelStartsAtZero_(false) {
  setSize(64, 64);
}

InstrumentGrid::~InstrumentGrid() {}

void InstrumentGrid::setConfig(const LightConfig& config) {
  ScopedLock l(lock_);

  background_ = config.visualizer.background;

  getParentComponent()->setVisible(true); // Fix this.
  setPaintingIsUnclipped(config.visualizer.instrument.paintUnclipped);

  setLightCount(config.count);
  setLayout(config.visualizer.layout, config.visualizer.instrument.size,
            config.visualizer.padding, config.visualizer.instrument.padding,
            config.visualizer.instrument.labelPadding);
}

void InstrumentGrid::setLayout(
    const Point& lay, const Point& size, const Point& padding,
    const Point& instrumentPadding, const Point& labelPadding) {
  ScopedLock l(lock_);
  padding_ = padding;
  size_ = size;
  layout_ = lay;
  instrumentPadding_ = instrumentPadding;
  labelPadding_ = labelPadding;
  layout();
}

void InstrumentGrid::layout() {
  int left = padding_.x;
  int top = padding_.y;
  int columns = layout_.x;
  int rows = layout_.y;

  int w = size_.x + instrumentPadding_.x;
  int h = size_.y + instrumentPadding_.y;
  int i = 0;
  for (int y = 0; y < rows and i < instruments_.size(); ++y) {
    for (int x = 0; x < columns and i < instruments_.size(); ++x) {
      auto& instr = instruments_[i++];
      instr->setLabelPadding(labelPadding_.x, labelPadding_.y);
      instr->setBounds(left + x * w, top + y * h, size_.x, size_.y);
    }
  }

  int screenWidth = left + w * columns + padding_.x,
    screenHeight = top + h * rows + padding_.y;

  setSize(screenWidth, screenHeight);
}

void InstrumentGrid::setLights(const ColorList& lights) {
  MessageManagerLock l;
  for (int i = 0; i < lights.size(); ++i)
    instruments_[i]->setColor(lights[i]);
}

void InstrumentGrid::paint(Graphics& g) {
  g.fillAll(background_);
}

void InstrumentGrid::setPaintingIsUnclipped(bool isUnclipped) {
  ScopedLock l(lock_);
  if (isUnclipped != isUnclipped_) {
    isUnclipped_ = isUnclipped;
    for (auto& i: instruments_)
      i->setPaintingIsUnclipped(isUnclipped);
  }
}

void InstrumentGrid::setLabelStartsAtZero(bool startsAtZero) {
  ScopedLock l(lock_);
  if (startsAtZero != labelStartsAtZero_) {
    labelStartsAtZero_ = startsAtZero;
    int delta = labelStartsAtZero_ ? 0 : 1;
    for (int i = 0; i < instruments_.size(); ++i)
      instruments_[i]->setLabel(String(i + delta));
  }
}

void InstrumentGrid::setLightCount(int count) {
  ScopedLock l(lock_);
  int oldCount = instruments_.size();

  if (count == oldCount)
    return;

  int delta = labelStartsAtZero_ ? 0 : 1;
  instruments_.resize(count);
  for (int i = oldCount; i < count; ++i) {
    auto inst = new InstrumentComponent;
    instruments_[i].reset(inst);
    inst->setPaintingIsUnclipped(isUnclipped_);
    inst->setLabelPadding(labelPadding_.x, labelPadding_.y);
    inst->setLabel(String(i + delta));
    addAndMakeVisible(inst);
  }
}

void InstrumentGrid::setBackground(const Colour& c) {
  ScopedLock l(lock_);
  background_ = c;
}

}  // namespace echomesh

