#include <algorithm>
#include <map>

#include "echomesh/color/Colors.h"

using namespace std;

namespace echomesh {

namespace {

const float NEAR = 1.0 / powf(2.0, 16);

bool near(float f1, float f2) {
  return fabsf(f1 - f2) < NEAR;
}

int compareColours(const Colour& x, const Colour& y) {
  auto xa = x.getARGB();
  auto ya = y.getARGB();
  auto xrgb = xa & 0xffffff;
  auto yrgb = ya & 0xffffff;
  if (xrgb < yrgb)
    return -1;
  if (xrgb > yrgb)
    return 1;
  if (xa < ya)
    return -1;
  if (xa > ya)
    return 1;
  return 0;
}

struct Compare {
  bool operator()(const Colour& x, const Colour& y) const {
    return compareColours(x, y) < 0;
  }
};

struct ColorNamer {
  std::map<String, Colour> stringToColor_;
  std::map<Colour, String, Compare> colorToString_;

  void add(const String& s, uint32 h) {
    add(s, Colour(h));
  }

  void add(const String& s, const Colour& c) {
    stringToColor_[s] = c;
    colorToString_[c] = s;
  }
};

ColorNamer makeNamer() {
  ColorNamer namer;

  namer.add("aliceblue", 0xfff0f8ff);
  namer.add("antiquewhite", 0xfffaebd7);
  namer.add("aqua", 0xff00ffff);
  namer.add("aquamarine", 0xff7fffd4);
  namer.add("azure", 0xfff0ffff);
  namer.add("beige", 0xfff5f5dc);
  namer.add("bisque", 0xffffe4c4);
  namer.add("black", 0xff000000);
  namer.add("blanchedalmond", 0xffffebcd);
  namer.add("blue", 0xff0000ff);
  namer.add("blueviolet", 0xff8a2be2);
  namer.add("brown", 0xffa52a2a);
  namer.add("burlywood", 0xffdeb887);
  namer.add("cadetblue", 0xff5f9ea0);
  namer.add("chartreuse", 0xff7fff00);
  namer.add("chocolate", 0xffd2691e);
  namer.add("coral", 0xffff7f50);
  namer.add("cornflowerblue", 0xff6495ed);
  namer.add("cornsilk", 0xfffff8dc);
  namer.add("crimson", 0xffdc143c);
  namer.add("cyan", 0xff00ffff);
  namer.add("darkblue", 0xff00008b);
  namer.add("darkcyan", 0xff008b8b);
  namer.add("darkgoldenrod", 0xffb8860b);
  namer.add("darkgreen", 0xff006400);
  namer.add("darkgrey", 0xff555555);
  namer.add("darkkhaki", 0xffbdb76b);
  namer.add("darkmagenta", 0xff8b008b);
  namer.add("darkolivegreen", 0xff556b2f);
  namer.add("darkorange", 0xffff8c00);
  namer.add("darkorchid", 0xff9932cc);
  namer.add("darkred", 0xff8b0000);
  namer.add("darksalmon", 0xffe9967a);
  namer.add("darkseagreen", 0xff8fbc8f);
  namer.add("darkslateblue", 0xff483d8b);
  namer.add("darkslategrey", 0xff2f4f4f);
  namer.add("darkturquoise", 0xff00ced1);
  namer.add("darkviolet", 0xff9400d3);
  namer.add("deeppink", 0xffff1493);
  namer.add("deepskyblue", 0xff00bfff);
  namer.add("dimgrey", 0xff696969);
  namer.add("dodgerblue", 0xff1e90ff);
  namer.add("firebrick", 0xffb22222);
  namer.add("floralwhite", 0xfffffaf0);
  namer.add("forestgreen", 0xff228b22);
  namer.add("fuchsia", 0xffff00ff);
  namer.add("gainsboro", 0xffdcdcdc);
  namer.add("gold", 0xffffd700);
  namer.add("goldenrod", 0xffdaa520);
  namer.add("green", 0xff00ff00);
  namer.add("greenyellow", 0xffadff2f);
  namer.add("grey", 0xff808080);
  namer.add("honeydew", 0xfff0fff0);
  namer.add("hotpink", 0xffff69b4);
  namer.add("indianred", 0xffcd5c5c);
  namer.add("indigo", 0xff4b0082);
  namer.add("ivory", 0xfffffff0);
  namer.add("khaki", 0xfff0e68c);
  namer.add("lavender", 0xffe6e6fa);
  namer.add("lavenderblush", 0xfffff0f5);
  namer.add("lemonchiffon", 0xfffffacd);
  namer.add("lightblue", 0xffadd8e6);
  namer.add("lightcoral", 0xfff08080);
  namer.add("lightcyan", 0xffe0ffff);
  namer.add("lightgoldenrodyellow", 0xfffafad2);
  namer.add("lightgreen", 0xff90ee90);
  namer.add("lightgrey", 0xffd3d3d3);
  namer.add("lightpink", 0xffffb6c1);
  namer.add("lightsalmon", 0xffffa07a);
  namer.add("lightseagreen", 0xff20b2aa);
  namer.add("lightskyblue", 0xff87cefa);
  namer.add("lightslategrey", 0xff778899);
  namer.add("lightsteelblue", 0xffb0c4de);
  namer.add("lightyellow", 0xffffffe0);
  namer.add("limegreen", 0xff32cd32);
  namer.add("linen", 0xfffaf0e6);
  namer.add("magenta", 0xffff00ff);
  namer.add("maroon", 0xff800000);
  namer.add("mediumaquamarine", 0xff66cdaa);
  namer.add("mediumblue", 0xff0000cd);
  namer.add("mediumorchid", 0xffba55d3);
  namer.add("mediumpurple", 0xff9370db);
  namer.add("mediumseagreen", 0xff3cb371);
  namer.add("mediumslateblue", 0xff7b68ee);
  namer.add("mediumspringgreen", 0xff00fa9a);
  namer.add("mediumturquoise", 0xff48d1cc);
  namer.add("mediumvioletred", 0xffc71585);
  namer.add("midnightblue", 0xff191970);
  namer.add("mintcream", 0xfff5fffa);
  namer.add("mistyrose", 0xffffe4e1);
  namer.add("navajowhite", 0xffffdead);
  namer.add("navy", 0xff000080);
  namer.add("none", 0x00000000);
  namer.add("oldlace", 0xfffdf5e6);
  namer.add("olive", 0xff808000);
  namer.add("olivedrab", 0xff6b8e23);
  namer.add("orange", 0xffffa500);
  namer.add("orangered", 0xffff4500);
  namer.add("orchid", 0xffda70d6);
  namer.add("palegoldenrod", 0xffeee8aa);
  namer.add("palegreen", 0xff98fb98);
  namer.add("paleturquoise", 0xffafeeee);
  namer.add("palevioletred", 0xffdb7093);
  namer.add("papayawhip", 0xffffefd5);
  namer.add("peachpuff", 0xffffdab9);
  namer.add("peru", 0xffcd853f);
  namer.add("pink", 0xffffc0cb);
  namer.add("plum", 0xffdda0dd);
  namer.add("powderblue", 0xffb0e0e6);
  namer.add("purple", 0xff800080);
  namer.add("red", 0xffff0000);
  namer.add("rosybrown", 0xffbc8f8f);
  namer.add("royalblue", 0xff4169e1);
  namer.add("saddlebrown", 0xff8b4513);
  namer.add("salmon", 0xfffa8072);
  namer.add("sandybrown", 0xfff4a460);
  namer.add("seagreen", 0xff2e8b57);
  namer.add("seashell", 0xfffff5ee);
  namer.add("sienna", 0xffa0522d);
  namer.add("silver", 0xffc0c0c0);
  namer.add("skyblue", 0xff87ceeb);
  namer.add("slateblue", 0xff6a5acd);
  namer.add("slategrey", 0xff708090);
  namer.add("snow", 0xfffffafa);
  namer.add("springgreen", 0xff00ff7f);
  namer.add("steelblue", 0xff4682b4);
  namer.add("tan", 0xffd2b48c);
  namer.add("teal", 0xff008080);
  namer.add("thistle", 0xffd8bfd8);
  namer.add("tomato", 0xffff6347);
  namer.add("turquoise", 0xff40e0d0);
  namer.add("violet", 0xffee82ee);
  namer.add("wheat", 0xfff5deb3);
  namer.add("white", 0xffffffff);
  namer.add("whitesmoke", 0xfff5f5f5);
  namer.add("yellow", 0xffffff00);
  namer.add("yellowgreen", 0xff9acd32);

  for (auto i = 1; i < 100; ++i) {
    auto g = (i * 255) / 100;
    namer.add("grey " + String(i), Colour(g, g, g));
  }

  return namer;
}

static const ColorNamer NAMER = makeNamer();

} // namespace

bool FColor::operator==(const FColor& other) const {
  return
      near(RGB::red(*this), RGB::red(other)) and
      near(RGB::green(*this), RGB::green(other)) and
      near(RGB::blue(*this), RGB::blue(other)) and
      near(alpha_, other.alpha_);
}

FColor FColor::NO_COLOR(0.0f, 0.0f, 0.0f, 0.0f);

FColor FColor::toHSB() const {
  const auto brightness = jmax(RGB::red(*this), RGB::green(*this), RGB::blue(*this));
  auto hue = 0.0f, saturation = 0.0f;

  if (not near(brightness, 0.0)) {
    const auto darkest = jmin(RGB::red(*this), RGB::green(*this), RGB::blue(*this));
    const auto range = brightness - darkest;
    saturation = range / brightness;

    if (not near(saturation, 0.0)) {
      const float r = (brightness - RGB::red(*this)) / range;
      const float g = (brightness - RGB::green(*this)) / range;
      const float b = (brightness - RGB::blue(*this)) / range;

      if (near(RGB::red(*this), brightness))
        hue = b - g;
      else if (near(RGB::green(*this), brightness))
        hue = 2.0f + r - b;
      else
        hue = 4.0f + g - r;

      hue /= 6.0f;

      if (hue < 0)
        hue += 1.0f;
    }
  }
  return FColor(hue, saturation, brightness, alpha_);
}


// from http://www.cs.rit.edu/~ncs/color/t_convert.html
void HSVtoRGB(float h, float s, float v) {
  float r, g, b;
 	if (s == 0) {
		// achromatic (grey)
		r = g = b = v;
	} else {
    h *= 6;			// sector 0 to 5
    int i = floor(h);
    auto f = h - i;			// factorial part of h
    auto p = v * (1 - s);
    auto q = v * (1 - s * f);
    auto t = v * (1 - s * (1 - f));

    switch(i) {
      case 0:
        r = v;
        g = t;
        b = p;
        break;

      case 1:
        r = q;
        g = v;
        b = p;
        break;

      case 2:
        r = p;
        g = v;
        b = t;
        break;

      case 3:
        r = p;
        g = q;
        b = v;
        break;

      case 4:
        r = t;
        g = p;
        b = v;
        break;

      case 5:
      default:
        r = v;
        g = p;
        b = q;
        break;
    }
  }

}

FColor FColor::fromHSB() const {
  return *this;
}

FColor FColor::toYIQ() const {
  return FColor(0.2999f * RGB::red(*this) + 0.5870f * RGB::green(*this) + 0.1140f * RGB::blue(*this),
                0.5957f * RGB::red(*this) - 0.2744f * RGB::green(*this) - 0.3212f * RGB::blue(*this),
                0.2114f * RGB::red(*this) - 0.5225f * RGB::green(*this) - 0.3113f * RGB::blue(*this),
                alpha_);
}

FColor FColor::fromYIQ() const {
  return FColor(RGB::red(*this) + 0.9563f * RGB::green(*this) + 0.6210f * RGB::blue(*this),
                RGB::red(*this) - 0.2721f * RGB::green(*this) - 0.6474f * RGB::blue(*this),
                RGB::red(*this) - 1.1070f * RGB::green(*this) + 1.7046f * RGB::blue(*this),
                alpha_);
}

bool fillColor(const String& cname, FColor* color) {
  auto name = cname.trim().toLowerCase().replace("gray", "grey");
  if (name.isEmpty())
    return false;

  if (name[0] == '#' or name.containsOnly("abcdef0123456789")) {
    *color = colorFromInt((uint32) name.getHexValue32());
    return true;
  }

  auto i = NAMER.stringToColor_.find(name);
  auto success = (i != NAMER.stringToColor_.end());
  if (success)
    *color = colourToRgb(i->second);
  return success;
}

FColor colorFromInt(uint32 argb) {
  return colourToRgb(Colour(argb));
}

string colorName(const FColor& fcolor) {
  Colour color = rgbToColour(fcolor);
  if (not color.getARGB())
    return "none";
  String suffix;
  FColor c;
  if (color.isOpaque()) {
    c = colourToRgb(color);
  } else {
    c = colourToRgb(color.withAlpha(1.0f));
    suffix = ", alpha=" + String(fcolor.alpha(), 3) + "]";
  }
  auto i = NAMER.colorToString_.find(rgbToColour(c));
  String name;
  if (i != NAMER.colorToString_.end()) {
    name = i->second;
    if (not suffix.isEmpty())
      name = "[" + name;
  } else {
    name = "[red=" + String(RGB::red(fcolor), 3) +
        ", green=" + String(RGB::green(fcolor), 3) +
        ", blue=" + String(RGB::blue(fcolor), 3);
    if (suffix.isEmpty())
      suffix += "]";
  }
  return (name + suffix).toStdString();
}

struct FCompare {
  bool operator()(const FColor& x, const FColor& y) const {
    return compareColors(x, y) < 0;
  }
};

void sortFColorList(vector<FColor>* colorList) {
  std::sort(colorList->begin(), colorList->end(), FCompare());
}

int countColorsInList(const FColorList& cl, const FColor& c) {
  return std::count(cl.begin(), cl.end(), c);
}

int indexColorInList(const FColorList& cl, const FColor& c) {
  auto i = std::find(cl.begin(), cl.end(), c);
  return i == cl.end() ? -1 : i - cl.begin();
}

void reverseFColorList(FColorList* cl) {
  std::reverse(cl->begin(), cl->end());
}

int compareColors(const FColor& x, const FColor& y) {
  if (RGB::red(x) < RGB::red(y))
    return -1;
  if (RGB::red(x) > RGB::red(y))
    return 1;
  if (RGB::green(x) < RGB::green(y))
    return -1;
  if (RGB::green(x) > RGB::green(y))
    return 1;
  if (RGB::blue(x) < RGB::blue(y))
    return -1;
  if (RGB::blue(x) > RGB::blue(y))
    return 1;
  if (x.alpha() < y.alpha())
    return -1;
  if (x.alpha() > y.alpha())
    return 1;
  return 0;
}

FColor interpolate(
    const FColor& begin, const FColor& end, float ratio) {
  auto br = RGB::red(begin), bg = RGB::green(begin), bb = RGB::blue(begin);
  auto er = RGB::red(end), eg = RGB::green(end), eb = RGB::blue(end);
  return FColor(br + ratio * (er - br),
                bg + ratio * (eg - bg),
                bb + ratio * (eb - bb));
}

void fillFColorList(
    FColorList* cl, const FColor& begin, const FColor& end, int size) {
  cl->resize(size);
  for (auto i = 0; i < size; ++i)
    cl->at(i) = interpolate(begin, end, i / (size - 1.0));
}

}  // namespace echomesh
