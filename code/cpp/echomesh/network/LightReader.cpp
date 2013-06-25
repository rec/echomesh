#include <stdio.h>
#include <fstream>
#include <iostream>
#include <string>

#include "base64/base64.h"
#include "echomesh/base/Quit.h"
#include "echomesh/component/LightingWindow.h"
#include "echomesh/network/LightReader.h"
#include "echomesh/network/SocketLineGetter.h"
#include "echomesh/util/GetDevice.h"
#include "rec/util/thread/MakeCallback.h"
#include "rec/util/thread/LockedCallback.h"
#include "rec/util/thread/CallAsync.h"

namespace echomesh {

using namespace std;
using namespace rec::util::thread;

#if 0 && JUCE_LINUX

static const char DEVICE_NAME[] = "/dev/spidev0.0";
const int LATCH_BYTE_COUNT = 3;
uint8 LATCH[LATCH_BYTE_COUNT] = {0};

#endif

static const string DEFAULT_CONFIG =
  "data:\n"
  "  light:\n"
  "    brightness: 100%\n"
  "    count: 256\n"
  "    enable: false\n"
  "    hardware: {enable: true, local: true, period: 5ms, rgb_order: rgb}\n"
  "    visualizer:\n"
  "      background: [1.0, 1.0, 1.0]\n"
  "      enable: true\n"
  "      instrument:\n"
  "        background: [0.3764705882352941, 0.3764705882352941, 0.3764705882352941]\n"
  "        border:\n"
  "          color: [0.0, 0.0, 0.0]\n"
  "          width: 1\n"
  "        label: false\n"
  "        label_padding: [2, 2]\n"
  "        label_starts_at_zero: false\n"
  "        padding: [2, 2]\n"
  "        paint_unclipped: false\n"
  "        shape: circle\n"
  "        size: [12, 12]\n"
  "      layout: [16, 16]\n"
  "      padding: [3, 3]\n"
  "      period: 10ms\n"
  "      show: true\n"
  "      top_left: [0, 44]\n"
  "      type: client\n"
  "      visualizer_closes_echomesh: true\n"
  "  midi:\n"
  "    input: {external: true, index: -1, name: from Max}\n"
  "    output: {external: true, index: -1, name: to Max}\n"
  "type: config\n"
  "---\n"
;


LightReader::LightReader(LightingWindow* wind, const String& commandLine)
    : ReadThread(commandLine),
      lightingWindow_(wind),
#if 0 && JUCE_LINUX
      file_(fopen(DEVICE_NAME, "w")),
#endif
      compressed_(true),
      midiInput_(new ConfigMidiInput(this)),
      midiOutput_(new ConfigMidiOutput) {
  addHandler("clear", methodCallback(this, &LightReader::clear));
  addHandler("config", methodCallback(this, &LightReader::config));
  addHandler("light", methodCallback(this, &LightReader::light));
  addHandler("midi", methodCallback(this, &LightReader::midi));
  addHandler("quit", methodCallback(this, &LightReader::quit));

  if (commandLine.isEmpty()) {
    lightingWindow_->setRunningInTest();
    parse(DEFAULT_CONFIG);
  }
}

LightReader::~LightReader() {
#if 0 && JUCE_LINUX
  fclose(file_);
#endif
}

void LightReader::handleIncomingMidiMessage(MidiInput*, const MidiMessage& msg) {
  log("Incoming MIDI message");
  if (SocketLineGetter* getter = SocketLineGetter::instance()) {
    YAML::Emitter out;

    out << YAML::BeginMap
        << YAML::Key << "type"
        << YAML::Value << "midi"
        << YAML::Key << "data"
        << YAML::Value << YAML::BeginSeq;

    int size = msg.getRawDataSize();
    const uint8* data = msg.getRawData();
    for (int i = 0; i < size; ++i)
      out << static_cast<int>(data[i]);

    out << YAML::EndSeq << YAML::EndMap;

    getter->writeSocket(out.c_str(), out.size());
  }
}

void LightReader::quit() {
  ::echomesh::quit();
}

void LightReader::clear() {
  for (int i = 0; i < colors_.size(); ++i)
    colors_[i] = Colours::black;

  displayLights();
}

void LightReader::enforceSizes() {
  if (colors_.size() != config_.light.count)
    colors_.resize(config_.light.count, Colours::black);

  if (colorBytes_.size() != 3 * config_.light.count)
    colorBytes_.resize(3 * config_.light.count, 0x80);
}

void LightReader::config() {
  const YAML::Node& data = node_["data"];
  data >> config_;
  enforceSizes();

  for (int i = 0; i < 3; ++i)
    rgbOrder_[i] = config_.light.hardware.rgbOrder.find("rgb"[i]);

  lightingWindow_->setConfig(config_.light);
  midiInput_->setConfig(config_.midi.input);
  midiOutput_->setConfig(config_.midi.output);
}

static MidiMessage makeMidiMessage(const YAML::Node& data) {
  int size = data.size();
  int b;
  vector<uint8> bytes(size);
  for (int i = 0; i < size; ++i) {
    data[i] >> b;
    bytes[i] = static_cast<uint8>(b);
  }
  return MidiMessage(&bytes[0], size);
}

void LightReader::midi() {
  midiOutput_->sendMessageNow(makeMidiMessage(node_["data"]));
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
  if (config_.light.hardware.local)  // Do the lights in Python.
    return;

  if (compressed_) {
    for (int i = 0; i < config_.light.count; ++i) {
      const Colour& color = colors_[i];
      uint8* light = &colorBytes_[3 * i];
      light[rgbOrder_[0]] = getSpiColor(color.getRed());
      light[rgbOrder_[1]] = getSpiColor(color.getGreen());
      light[rgbOrder_[2]] = getSpiColor(color.getBlue());
    }
  } else {
    for (int i = 0; i < config_.light.count; ++i) {
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

  if (lights2.size() != 3 * config_.light.count) {
    String msg = "Size " + String(int(lights.size())) +
      ", count " + String(config_.light.count);
    log(msg);
    return;
  }

  const char* data = lights2.data();
  const uint8* bytes = reinterpret_cast<const uint8*>(data);

  for (int i = 0; i < config_.light.count; ++i)
    colors_[i] = Colour(bytes[3 * i], bytes[3 * i + 1], bytes[3 * i + 2]);

  displayLights();
}

}  // namespace echomesh
