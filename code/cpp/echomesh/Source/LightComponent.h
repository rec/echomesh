#ifndef __LIGHT_COMPONENT__
#define __LIGHT_COMPONENT__

#include "../JuceLibraryCode/JuceHeader.h"
#include "disallow.h"
#include <iostream>
#include <string>
#include <stdio.h>
#include <vector>

#include "../JuceLibraryCode/JuceHeader.h"

typedef unsigned char byte;

struct Light {
  byte rgb_[3];
};

typedef std::vector<Light> LightList;

class LightComponent : public Component {
 public:
  LightComponent()
      : count_(16),
        width_(4),
        height_(4),
        leftPadding_(5),
        topPadding_(10),
        lightPaddingX_(3),
        lightPaddingY_(3),
        buttonWidth_(16),
        buttonHeight_(16),
        colors_(count_, Colours::black) {
    setSize (500, 400);
  }
  ~LightComponent() {}

  void paint (Graphics& g) {
    g.fillAll(Colours::white);
    for (int col = 0; col < width_; ++col) {
      for (int row = 0; row < height_; ++row) {
        int x = leftPadding_ + col * (buttonWidth_ + lightPaddingX_);
        int y = topPadding_ + row * (buttonHeight_ + lightPaddingY_);
        int pos = width_ * row + col;
        Colour color = (pos < colors_.size()) ? colors_[pos] : Colours::black;
        std::cout << "a: " << row << ", " << col << ", "
                  << color.toDisplayString(false) << "\n";
        g.setColour(color);
        g.fillEllipse(x, y, buttonWidth_, buttonHeight_);
      }
    }
  }

  void setLights(const StringArray& lights) {
    size_t size = lights.size() / 3;
    size = jmin(colors_.size(), size);
    for (int i = 0; i < size; ++i) {
      uint8 r = static_cast<uint8>(lights[3 * i].getIntValue());
      uint8 g = static_cast<uint8>(lights[3 * i + 1].getIntValue());
      uint8 b = static_cast<uint8>(lights[3 * i + 2].getIntValue());
      colors_[i] = Colour(r, g, b);
      std::cout << "i: " << i << ", r=" << (int) r << ", g=" << (int) g <<  ", b=" << (int) b << "\n";
    }
    MessageManagerLock l;
    repaint();
  }

  void setLayout(const StringArray& layout) {
    colors_.resize(layout[0].getIntValue(), Colours::black);
    width_ = layout[1].getIntValue();
    height_ = layout[2].getIntValue();

    MessageManagerLock l;
    repaint();
  }

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


#endif  // __LIGHT_COMPONENT__
