#include <stdio.h>
#include <fstream>
#include <iostream>
#include <string>

#include "base64/base64.h"
#include "echomesh/component/LightingWindow.h"
#include "echomesh/network/LightReader.h"
#include "rec/util/thread/MakeCallback.h"

namespace echomesh {

namespace {

struct QuitMessage : public CallbackMessage {
  virtual void messageCallback() {
    JUCEApplication::quit();
  };
};

}

using namespace std;
using namespace rec::util::thread;

#if 0 && JUCE_LINUX

static const char DEVICE_NAME[] = "/dev/spidev0.0";
const int LATCH_BYTE_COUNT = 3;
uint8 LATCH[LATCH_BYTE_COUNT] = {0};

#endif

LightReader::LightReader(LightingWindow* wind, const String& commandLine)
    : ReadThread(commandLine),
      lightingWindow_(wind),
      compressed_(true),
#if 0 && JUCE_LINUX
      file_(fopen(DEVICE_NAME, "w")),
#endif
      configReceived_(false) {
  addHandler("clear", methodCallback(this, &LightReader::clear));
  addHandler("config", methodCallback(this, &LightReader::config));
  addHandler("light", methodCallback(this, &LightReader::light));
  addHandler("quit", methodCallback(this, &LightReader::quit));
  addHandler("show", methodCallback(wind, &LightingWindow::setVisible, true));
  addHandler("hide", methodCallback(wind, &LightingWindow::setVisible, false));
}

LightReader::~LightReader() {
#if 0 && JUCE_LINUX
  fclose(file_);
#endif
}

void LightReader::quit() {
  (new QuitMessage)->post();
}

void LightReader::clear() {
  for (int i = 0; i < colors_.size(); ++i)
    colors_[i] = Colours::black;

  displayLights();
}

void LightReader::enforceSizes() {
  if (colors_.size() != config_.count)
    colors_.resize(config_.count, Colours::black);

  if (colorBytes_.size() != 3 * config_.count)
    colorBytes_.resize(3 * config_.count, 0x80);
}

void LightReader::config() {
  const YAML::Node& data = node_["data"];
  data >> config_;
  enforceSizes();

  for (int i = 0; i < 3; ++i)
    rgbOrder_[i] = config_.hardware.rgbOrder.find("rgb"[i]);

  lightingWindow_->setConfig(config_);

  if (not configReceived_) {
    configReceived_ = true;
    MessageManagerLock l;
    lightingWindow_->setVisible(true);
  }
}

inline uint8 getSpiColor(uint8 color) {
  return color / 2 + 0x80;
}

uint8 LightReader::getLedColor(float color) const {
  int c = static_cast<int>((color * brightness_ + 1) * 0x80);
  return static_cast<uint8>(jmin(c, 0xFF));
}

void LightReader::displayLights() {
  lightingWindow_->setLights(colors_);
  if (config_.hardware.local)  // Do the lights in Python.
    return;

  if (compressed_) {
    for (int i = 0; i < config_.count; ++i) {
      const Colour& color = colors_[i];
      uint8* light = &colorBytes_[3 * i];
      light[rgbOrder_[0]] = getSpiColor(color.getRed());
      light[rgbOrder_[1]] = getSpiColor(color.getGreen());
      light[rgbOrder_[2]] = getSpiColor(color.getBlue());
    }
  } else {
    for (int i = 0; i < config_.count; ++i) {
      const Colour& color = colors_[i];
      uint8* light = &colorBytes_[3 * i];
      light[rgbOrder_[0]] = getLedColor(color.getFloatRed());
      light[rgbOrder_[1]] = getLedColor(color.getFloatGreen());
      light[rgbOrder_[2]] = getLedColor(color.getFloatBlue());
    }
  }

#if 0 && JUCE_LINUX
  fwrite(&colorBytes_.front(), 1, colorBytes_.size(), file_);
  fflush(file_);
  fwrite(LATCH, 1, 3, file_);
  fflush(file_);
#endif
}

void LightReader::light() {
  compressed_ = true;
  string lights;
  const YAML::Node& lightNode = node_["data"];
  if (lightNode.size() == 1) {
    lightNode[0] >> lights;
  } else {
    for (int i = 0; i < lightNode.size(); ++i) {
      string lt;
      lightNode[i] >> lt;
      lights += lt;
    }
  }

  string lights2 = base64::decode(lights);

  if (lights2.size() != 3 * config_.count) {
    String msg = "Size " + String(int(lights.size())) +
      ", count " + String(config_.count);
    log(msg);
    return;
  }

  const char* data = lights2.data();
  const uint8* bytes = reinterpret_cast<const uint8*>(data);

  for (int i = 0; i < config_.count; ++i)
    colors_[i] = Colour(bytes[3 * i], bytes[3 * i + 1], bytes[3 * i + 2]);

  displayLights();
}

}  // namespace echomesh
