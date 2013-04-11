#ifndef __LIGHT_COMPONENT__
#define __LIGHT_COMPONENT__

#include "Echomesh.h"

namespace echomesh {

typedef unsigned char byte;

struct Light {
  byte rgb_[3];
};

typedef std::vector<Light> LightList;

class LightComponent : public Component {
 public:
  LightComponent();
  ~LightComponent() {}

  void paint(Graphics& g);

  void setColors(const std::vector<Colour>&);

  void setLights(const StringArray&);

  void setLayout(const StringArray&);

 private:
  int count_;
  int width_;
  int height_;
  int leftPadding_;
  int topPadding_;
  int lightPaddingX_;
  int lightPaddingY_;
  int buttonWidth_;
  int buttonHeight_;

  std::vector<Colour> colors_;

  JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (LightComponent)
};

}  // namespace echomesh

#endif  // __LIGHT_COMPONENT__
