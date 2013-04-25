#ifndef __LIGHT_CONFIG__
#define __LIGHT_CONFIG__

#include "yaml-cpp/yaml.h"

#include "echomesh/Echomesh.h"

namespace echomesh {

struct Point {
  int x;
  int y;
};

struct Border {
  Colour color;
  int width;
};

struct LightDisplay {
  Colour background;
  Border border;
  bool isRect;
  bool label;
  Point labelPadding;
  Point padding;
  Point size;
  string shape;
};

struct Padding {
  int top;
  int left;
  int bottom;
  int right;
};

struct Display {
  Colour background;
  Point layout;
  Padding padding;
  LightDisplay light;
};

struct LightConfig {
  int count;
  string rgbOrder;

  Display display;
};

typedef uint8 ColorBytes[3];
typedef std::vector<ColorBytes> ColorByteBank;
typedef std::vector<Colour> ColorList;
typedef std::vector<uint8> ByteList;

void operator>>(const YAML::Node&, Colour&);
void operator>>(const YAML::Node&, Point&);
void operator>>(const YAML::Node&, Border&);
void operator>>(const YAML::Node&, LightDisplay&);
void operator>>(const YAML::Node&, Padding&);
void operator>>(const YAML::Node&, Display&);
void operator>>(const YAML::Node&, LightConfig&);
void operator>>(const YAML::Node&, ColorBytes&);
void operator>>(const YAML::Node&, ColorList&);

}  // namespace echomesh

#endif  // __LIGHT_CONFIG__
