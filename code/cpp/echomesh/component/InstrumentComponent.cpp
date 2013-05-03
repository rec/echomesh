#include "/development/echomesh/code/cpp/echomesh/component/InstrumentComponent.h"

namespace echomesh {

InstrumentComponent::InstrumentComponent()
    : color_(Colours::black), labelColor_(Colours::white) {
  setPaintingIsUnclipped(true);
}

void InstrumentComponent::configure(const String& label,
                                    const Instrument& config) {
  ScopedLock l(lock_);
  config_ = config;
  label_ = label;
}

void InstrumentComponent::setColor(const Colour& c) {
  ScopedLock l(lock_);
  if (c == color_)
    return;

  color_ = c;
  static const int GREY = (3 * 0xFF) / 2;
  uint8 r = color_.getRed();
  uint8 g = color_.getGreen();
  uint8 b = color_.getBlue();
  labelColor_ = (r + g + b >= GREY) ? Colours::black : Colours::white;
  repaint();
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

