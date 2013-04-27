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

static const char DEVICE_NAME[] = "/dev/spidev0.0";
const int LATCH_BYTE_COUNT = 3;
uint8 LATCH[LATCH_BYTE_COUNT] = {0};

LightReader::LightReader(LightingWindow* window, const String& commandLine)
    : ReadThread(commandLine),
      lightingWindow_(window),
      compressed_(true)
#if JUCE_LINUX
, file_(fopen(DEVICE_NAME, "w"))
#endif
{
  registerCallback("clear", methodCallback(this, &LightReader::clear));
  registerCallback("clight", methodCallback(this, &LightReader::clight));
  registerCallback("config", methodCallback(this, &LightReader::config));
  registerCallback("light", methodCallback(this, &LightReader::light));
  registerCallback("quit", methodCallback(this, &LightReader::quit));
}

LightReader::~LightReader() {
#if JUCE_LINUX
  fclose(file_);
#endif
}

void LightReader::quit() {
  log("quitting");
  (new QuitMessage)->post();
  log("done");
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
  log("config.");
  data >> config_;
  enforceSizes();

  for (int i = 0; i < 3; ++i)
    rgbOrder_[i] = config_.rgbOrder.find("rgb"[i]);
  log("set config set light.");
  lightingWindow_->setConfig(config_);
  log("config done.");
}

inline uint8 getSpiColor(uint8 color) {
  return color / 2 + 0x80;
}

uint8 LightReader::getLedColor(float color) const {
  int c = static_cast<int>((color * brightness_ + 1) * 0x80);
  return static_cast<uint8>(jmin(c, 0xFF));
}

void LightReader::light() {
  compressed_ = false;
  const YAML::Node& data = node_["data"];
  data["colors"] >> colors_;
  data["brightness"] >> brightness_;
  enforceSizes();
  displayLights();
}

void LightReader::displayLights() {
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

#if JUCE_LINUX
  fwrite(&colorBytes_.front(), 1, colorBytes_.size(), file_);
  fflush(file_);
  fwrite(LATCH, 1, 3, file_);
  fflush(file_);
#endif
  lightingWindow_->setLights(colors_);
}

void LightReader::clight() {
  compressed_ = true;
  string lights;
  node_["data"] >> lights;

  string lights2 = base64::decode(lights);

  if (lights2.size() != 3 * config_.count) {
    throw Exception("Size " + String(int(lights.size()) +
                                     ", count " + config_.count));
  }

  const char* data = lights2.data();
  const uint8* bytes = reinterpret_cast<const uint8*>(data);

  for (int i = 0; i < config_.count; ++i)
    colors_[i] = Colour(bytes[3 * i], bytes[3 * i + 1], bytes[3 * i + 2]);

  displayLights();
}

}  // namespace echomesh
