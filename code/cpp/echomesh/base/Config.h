#ifndef __ECHOMESH_LIGHT_CONFIG__
#define __ECHOMESH_LIGHT_CONFIG__

#include "yaml-cpp/yaml.h"

#include "echomesh/base/Echomesh.h"

namespace echomesh {

// See echomesh/code/python/echomesh/config/config.yml

struct Point {
  int x;
  int y;
};

struct Border {
  Colour color;
  int width;
};

struct Instrument {
  Colour background;
  Border border;
  bool isRect;
  bool label;
  Point labelPadding;
  bool labelStartsAtZero;
  Point padding;
  bool paintUnclipped;
  Point size;
  string shape;
};

struct Visualizer {
  Colour background;
  Instrument instrument;
  Point layout;
  Point padding;
  Point topLeft;
  int period;
  bool show;
};

struct Hardware {
  bool enable;
  int period;
  bool local;
  string rgbOrder;
};

struct LightConfig {
  int count;
  bool enable;
  Hardware hardware;

  Visualizer visualizer;
};

struct OneMidiConfig {
  bool external;
  int index;
  string name;
};

struct MidiConfig {
  OneMidiConfig input, output;
};

struct Config {
  LightConfig light;
  MidiConfig midi;
};

typedef uint8 ColorBytes[3];
typedef std::vector<ColorBytes> ColorByteBank;
typedef std::vector<Colour> ColorList;
typedef std::vector<uint8> ByteList;

void operator>>(const YAML::Node&, ColorBytes&);
void operator>>(const YAML::Node&, ColorList&);
void operator>>(const YAML::Node&, Colour&);
void operator>>(const YAML::Node&, Point&);
void operator>>(const YAML::Node&, Border&);
void operator>>(const YAML::Node&, Instrument&);
void operator>>(const YAML::Node&, Visualizer&);
void operator>>(const YAML::Node&, Hardware&);
void operator>>(const YAML::Node&, OneMidiConfig&);
void operator>>(const YAML::Node&, MidiConfig&);
void operator>>(const YAML::Node&, LightConfig&);
void operator>>(const YAML::Node&, Config&);
void operator>>(const YAML::Node&, SampleTime&);
void operator>>(const YAML::Node&, RealTime&);

}  // namespace echomesh

#endif  // __ECHOMESH_LIGHT_CONFIG__
