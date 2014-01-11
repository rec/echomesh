#include "rec/util/STL.h"
#include "echomesh/color/FColorList.h"
#include "echomesh/color/RGB.h"
#include "echomesh/component/InstrumentGrid.h"
#include "echomesh/util/RunOnMessageThread.h"

namespace echomesh {

static const int TOP_TWEAK = 5;
static const int LEFT_TWEAK = 5;

InstrumentGrid::InstrumentGrid()
    : isUnclipped_(false),
      labelStartsAtZero_(false),
      showLabel_(false),
      background_(Colours::white),
      columns_(16),
      rows_(16),
      layout_(16, 16),
      size_(16, 16),
      padding_(5, 5),
      instrumentPadding_(2, 2),
      labelPadding_(2, 2) {
  setSize(64, 64);
  MessageManagerLock l;
  layout();
}

InstrumentGrid::~InstrumentGrid() {}

void InstrumentGrid::setLayout(
    const Point& lay, const Point& size, const Point& padding,
    const Point& instrumentPadding, const Point& labelPadding) {
  MessageManagerLock l;

  padding_ = padding;
  size_ = size;
  layout_ = lay;
  instrumentPadding_ = instrumentPadding;
  labelPadding_ = labelPadding;
  layout();
}

void InstrumentGrid::layout() {
  auto left = padding_.x;
  auto top = padding_.y;
  auto columns = layout_.x;
  auto rows = layout_.y;

  auto w = size_.x + instrumentPadding_.x;
  auto h = size_.y + instrumentPadding_.y;
  auto i = 0;
  for (auto y = 0; y < rows and i < instruments_.size(); ++y) {
    for (auto x = 0; x < columns and i < instruments_.size(); ++x) {
      auto& instr = instruments_[i++];
      instr->setLabelPadding(labelPadding_.x, labelPadding_.y);
      instr->setBounds(left + x * w, top + y * h, size_.x, size_.y);
      instr->setShowLabel(showLabel_);
    }
  }

  auto screenWidth = left + w * columns + padding_.x,
    screenHeight = top + h * rows + padding_.y;

  setSize(screenWidth, screenHeight);
}

void InstrumentGrid::paint(Graphics& g) {
  g.fillAll(background_);
}

void InstrumentGrid::setPaintingIsUnclipped(bool isUnclipped) {
  MessageManagerLock l;
  if (isUnclipped != isUnclipped_) {
    isUnclipped_ = isUnclipped;
    for (auto& i: instruments_)
      i->setPaintingIsUnclipped(isUnclipped);
  }
}

void InstrumentGrid::setLabelStartsAtZero(bool startsAtZero) {
  MessageManagerLock l;
  if (startsAtZero != labelStartsAtZero_) {
    labelStartsAtZero_ = startsAtZero;
    auto delta = labelStartsAtZero_ ? 0 : 1;
    for (auto i = 0; i < instruments_.size(); ++i)
      instruments_[i]->setLabel(String(i + delta));
  }
}

void InstrumentGrid::setLightCount(int count) {
  MessageManagerLock l;
  auto oldCount = instruments_.size();

  if (count == oldCount)
    return;

  cache_.resize(3 * count);

  auto delta = labelStartsAtZero_ ? 0 : 1;
  instruments_.resize(count);
  for (auto i = oldCount; i < count; ++i) {
    auto inst = make_unique<InstrumentComponent>();
    inst->setPaintingIsUnclipped(isUnclipped_);
    inst->setLabelPadding(labelPadding_.x, labelPadding_.y);
    inst->setLabel(String(uint32(i + delta)));
    addAndMakeVisible(inst.get());
    instruments_[i] = std::move(inst);
  }
  layout();
}

void InstrumentGrid::setBackground(const Colour& c) {
  MessageManagerLock l;
  background_ = c;
}

void InstrumentGrid::setShowLabel(bool showLabel) {
  MessageManagerLock l;
  if (showLabel != showLabel_) {
    showLabel_ = showLabel;
    for (auto& i: instruments_)
      i->setShowLabel(showLabel);
  }
}

int InstrumentGrid::getLightCount() const {
  MessageManagerLock l;
  return instruments_.size();
}

void InstrumentGrid::setLights(const char* lights) {
  MessageManagerLock l;
  for (auto i = 0; i < instruments_.size(); ++i) {
    Colour color(lights[3 * i], lights[3 * i + 1], lights[3 * i + 2]);
    instruments_[i]->setColor(color);
  }
}

void InstrumentGrid::setLights(const color::FColorList& colors) {
  MessageManagerLock l;
  auto size = jmin(colors.size(), instruments_.size());
  for (auto i = 0; i < size; ++i)
    instruments_[i]->setColor(colors.at(i).toColour());

  auto maxSize = jmax(colors.size(), instruments_.size());
  for (auto i = size; i < maxSize; ++i)
    instruments_[i]->setColor(Colours::black);
}

}  // namespace echomesh

