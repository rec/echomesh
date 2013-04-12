#include "/development/echomesh/code/cpp/echomesh/Source/LightComponent.h"

namespace echomesh {

LightComponent::LightComponent(DocumentWindow* window)
    : configEmpty_(true), window_(window) {
  setSize(500, 400);
}

void LightComponent::paint(Graphics& g) {
  g.fillAll(config_.display.background);  // TODO
  if (configEmpty_)
    return;

  boxSize_.x = light().size.x + light().padding.x;
  boxSize_.y = light().size.y + light().padding.y;

  int i = 0;
  bool isRect = light().shape.find("rect");

  for (int x = 0; x < layout().x; ++x) {
    for (int y = 0; y < layout().y; ++y) {
      if (++i >= config_.count)
        return;
      g.setColour(colors_[i]);
      Point p = {padding().left + x * boxSize_.x,
                 padding().top + y * boxSize_.y};
      if (isRect)
        g.fillRect(p.x, p.y, light().size.x, light().size.y);
      else
        g.fillEllipse(p.x, p.y, light().size.x, light().size.y);
    }
  }
}

void LightComponent::setLights(const ColorList& colors) {
  MessageManagerLock l;
  colors_ = colors;
  repaint();
}

void LightComponent::setConfig(const LightConfig& config) {
  MessageManagerLock l;
  config_ = config;
  configEmpty_ = false;
  boxSize_.x = light().size.x + light().padding.x;
  boxSize_.y = light().size.y + light().padding.y;

  Point screenSize = {
    padding().left + padding().right + boxSize_.x * layout().x,
    padding().top + padding().bottom + boxSize_.y * layout().y
  };

  setSize(screenSize.x, screenSize.y);
  window_->setSize(screenSize.x, screenSize.y);
}

}  // namespace echomesh

