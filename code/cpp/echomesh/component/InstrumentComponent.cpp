#include "/development/echomesh/code/cpp/echomesh/component/InstrumentComponent.h"

namespace echomesh {

InstrumentComponent::InstrumentComponent()
    : color_(Colours::black), labelColor_(Colours::white) {
}

void InstrumentComponent::configure(const String& label,
                                    const Instrument& config) {
  ScopedLock l(lock_);
  config_ = config;
  label_ = label;
}

void InstrumentComponent::setColor(uint8 r, uint8 g, uint8 b) {
  ScopedLock l(lock_);
  color_ = Colour(r, g, b);
  setLabel();
}

void InstrumentComponent::setColor(const Colour& c) {
  ScopedLock l(lock_);
  color_ = c;
  setLabel();
}

void InstrumentComponent::setLabel() {
  static const int GREY = (3 * 0xFF) / 2;
  uint8 r = color_.getRed();
  uint8 g = color_.getGreen();
  uint8 b = color_.getBlue();
  labelColor_ = (r + g + b >= GREY) ? Colours::black : Colours::white;
}

void InstrumentComponent::paint(Graphics& g) {
  ScopedLock l(lock_);
  Colour back, label;
  {
    back = color_;
    label = labelColor_;
  }

  g.setColour(back);
  Rectangle<int> b = getLocalBounds();
  if (config_.isRect)
    g.fillRect(b);
  else
    g.fillEllipse(b.getX(), b.getY(), b.getWidth(), b.getHeight());

  if (config_.label) {
    b.reduce(config_.labelPadding.x / 2, config_.labelPadding.y / 2);
    g.setColour(label);
    g.drawFittedText(label_, b, Justification::centred, 1);
  }
}

}  // namespace echomesh

