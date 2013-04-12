#include "/development/echomesh/code/cpp/echomesh/Source/ReadThread.h"

#include "LightComponent.h"

#include <iostream>
#include <string>
#include <stdio.h>

namespace echomesh {

#define JUCE_LINUX 1
// Only to make sure it compiles

static const char DEVICE_NAME[] = "/dev/spidev0.0";
const int LATCH_BYTE_COUNT = 3;
uint8 LATCH[LATCH_BYTE_COUNT] = {0};

ReadThread::ReadThread(LightComponent* light)
    : Thread("ReadThread"), lightComponent_(light)
#if JUCE_LINUX
, file_(fopen(DEVICE_NAME, "w"))
#endif
{
}

ReadThread::~ReadThread() {
#if JUCE_LINUX
  fclose(file_);
#endif
}

void ReadThread::run() {
  using namespace std;
  string s;
  String st;
  while (!feof(stdin)) {
    s.clear();
    getline(cin, s);
    if (s.find("---"))
      accum_.add(s.c_str());
    else
      handleMessage();
  }
}


void ReadThread::handleMessage() {
  String result = accum_.joinIntoString("\n");
  accum_.clear();

  std::string str(result.toUTF8());
  std::istringstream s(str);
  try {
    YAML::Parser parser(s);
    if (parser.GetNextDocument(node_))
      parseNode();
  } catch (YAML::Exception& e) {
    std::cout << e.what() << "\n";
  }
}

void ReadThread::parseNode() {
  std::string type;
  node_["type"] >> type;
  if (type == "quit") {
    signalThreadShouldExit();
    JUCEApplication::quit();
    return;
  }

  const YAML::Node& data = node_["data"];
  if (type == "light")
    parseLight(data);
  else if (type == "config")
    parseConfig(data);
}

void ReadThread::enforceSizes() {
  if (colors_.size() != config_.count)
    colors_.resize(config_.count, Colours::black);

  if (colorBytes_.size() != 3 * config_.count)
    colorBytes_.resize(3 * config_.count, 0x80);
#if 0
    static ColorBytes BLACK = {0x80, 0x80, 0x80};
    // TODO: why won't this compile?
    // bytes_.resize(config_.count, &BLACK);
    int i = bytes_.size();
    bytes_.resize(config_.count);
    for (; i < config_.count; ++i)
      bytes_[i] = BLACK;
  }
#endif
}

#define WHICH_RGB true

void ReadThread::parseConfig(const YAML::Node& data) {
  data >> config_;
  enforceSizes();

  for (int i = 0; i < 3; ++i) {
#if WHICH_RGB
    rgb_order_[i] = config_.rgb_order.find("rgb"[i]);
#else
    rgb_order_[i] = string("rgb").find(config_.rgb_order[i]);
#endif
  }
  lightComponent_->setConfig(config_);
}

void ReadThread::parseLight(const YAML::Node& data) {
  data >> colors_;
  enforceSizes();
  for (int i = 0; i < config_.count; ++i) {
    const Colour& color = colors_[i];
    uint8* light = &colorBytes_[3 * i];
    light[rgb_order_[0]] = color.getRed();
    light[rgb_order_[1]] = color.getGreen();
    light[rgb_order_[2]] = color.getBlue();
  }

#if JUCE_LINUX
  fwrite(&colorBytes_.front(), 1, colorBytes_.size(), file_);
  fflush(file_);
  fwrite(LATCH, 1, 3, file_);
  fflush(file_);
#endif
  lightComponent_->setLights(colors_);
}

}  // namespace echomesh
