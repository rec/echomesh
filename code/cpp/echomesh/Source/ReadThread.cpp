#include "/development/echomesh/code/cpp/echomesh/Source/ReadThread.h"

#include "LightComponent.h"

#include <iostream>
#include <string>
#include <stdio.h>

namespace echomesh {

// #define JUCE_LINUX 1
// Only to make sure it compiles

static const char DEVICE_NAME[] = "/dev/spidev0.0";
const int LATCH_BYTE_COUNT = 3;
uint8 LATCH[LATCH_BYTE_COUNT] = {0};

ReadThread::ReadThread(LightComponent* light)
    : Thread("ReadThread"), light_(light)
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
  if (type == "color")
    parseColor(data);
  else if (type == "settings")
    parseSettings(data);
}

void ReadThread::parseColor(const YAML::Node& data) {
  int input_size = data.size();
  int count = lights_.size() / 3;
  uint8* light = &lights_.front();
  for (int i = 0; i < count; ++i) {
    uint8 components[3];
    if (i < input_size) {
      const YAML::Node& color_node = data[i];
      for (int j = 0; j < 3; ++j)
        color_node[j] >> components[i];
    } else {
      memset(components, 3, '\0');
    }

    for (int j = 0; j < 3; ++j)
      *(light++) = 0x80 + (components[j] / 2);

    colors_[i] = Colour(components[0], components[1], components[2]);
  }
#if JUCE_LINUX
  fwrite(&lights_.front(), 3, count, file_);
  fflush(file_);
  fwrite(LATCH, 3, 1, file_);
  fflush(file_);
#endif
  light_->setColors(colors_);
}

void ReadThread::parseSettings(const YAML::Node& data) {
}

}  // namespace echomesh
