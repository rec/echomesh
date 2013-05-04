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
  int period;
  Colour background;
  Point layout;
  Point padding;
  Instrument instrument;
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

typedef uint8 ColorBytes[3];
typedef std::vector<ColorBytes> ColorByteBank;
typedef std::vector<Colour> ColorList;
typedef std::vector<uint8> ByteList;

void operator>>(const YAML::Node&, Colour&);
void operator>>(const YAML::Node&, Point&);
void operator>>(const YAML::Node&, Border&);
void operator>>(const YAML::Node&, Instrument&);
void operator>>(const YAML::Node&, Visualizer&);
void operator>>(const YAML::Node&, Hardware&);
void operator>>(const YAML::Node&, LightConfig&);
void operator>>(const YAML::Node&, ColorBytes&);
void operator>>(const YAML::Node&, ColorList&);

}  // namespace echomesh

#endif  // __ECHOMESH_LIGHT_CONFIG__
