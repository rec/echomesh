#include "echomesh/util/Colors.h"

using namespace std;

namespace echomesh {

namespace {

// From JuceLibraryCode/modules/juce_graphics/colour/juce_Colours.cpp

typedef pair<uint32, uint32> ColorPreset;

// (first value is the string's hashcode, second is ARGB)
ColorPreset COLOR_PRESETS[] = {
  make_pair(0x0001b891, 0xffff0000), /* red */
  make_pair(0x0001bfa1, 0xffd2b48c), /* tan */
  make_pair(0x002dcebc, 0xff00ffff), /* aqua */
  make_pair(0x002e305a, 0xff0000ff), /* blue */
  make_pair(0x002ed323, 0xff00ffff), /* cyan */
  make_pair(0x00308060, 0xffffd700), /* gold */
  make_pair(0x00308adf, 0xff808080), /* grey */
  make_pair(0x0032afd5, 0xff00ff00), /* lime */
  make_pair(0x00337bb6, 0xff000080), /* navy */
  make_pair(0x003472f8, 0xffcd853f), /* peru */
  make_pair(0x00348176, 0xffffc0cb), /* pink */
  make_pair(0x00348d94, 0xffdda0dd), /* plum */
  make_pair(0x0035f183, 0xfffffafa), /* snow */
  make_pair(0x0036425c, 0xff008080), /* teal */
  make_pair(0x00674f7e, 0xffffebcd), /* blanchedalmond */
  make_pair(0x056f5c58, 0xffba55d3), /* mediumorchid */
  make_pair(0x0590228f, 0xfff0ffff), /* azure */
  make_pair(0x05947fe4, 0xfff5f5dc), /* beige */
  make_pair(0x05978fff, 0xff000000), /* black */
  make_pair(0x059a8136, 0xffa52a2a), /* brown */
  make_pair(0x05a74431, 0xffff7f50), /* coral */
  make_pair(0x05e0cf03, 0xff008000), /* green */
  make_pair(0x05fef6a9, 0xfffffff0), /* ivory */
  make_pair(0x06149302, 0xfff0e68c), /* khaki */
  make_pair(0x06234efa, 0xfffaf0e6), /* linen */
  make_pair(0x064ee1db, 0xff808000), /* olive */
  make_pair(0x066be19e, 0xff7b68ee), /* mediumslateblue */
  make_pair(0x06bdbae7, 0xfff5deb3), /* wheat */
  make_pair(0x06bdcc29, 0xffffffff), /* white */
  make_pair(0x07556b71, 0xff9370db), /* mediumpurple */
  make_pair(0x0bb131e1, 0xfff4a460), /* sandybrown */
  make_pair(0x0fa260cf, 0xff5f9ea0), /* cadetblue */
  make_pair(0x10802ee6, 0xfff5f5f5), /* whitesmoke */
  make_pair(0x15e2ebc8, 0xffdb7093), /* palevioletred */
  make_pair(0x168eb32a, 0xff191970), /* midnightblue */
  make_pair(0x195756f0, 0xfffffacd), /* lemonchiffon */
  make_pair(0x20a2676a, 0xfffaebd7), /* antiquewhite */
  make_pair(0x21234e3c, 0xfffafad2), /* lightgoldenrodyellow */
  make_pair(0x25832862, 0xffff1493), /* deeppink */
  make_pair(0x28cb4834, 0xffeee8aa), /* palegoldenrod */
  make_pair(0x28e4ea70, 0xffadd8e6), /* lightblue */
  make_pair(0x28e58d39, 0xffe0ffff), /* lightcyan */
  make_pair(0x28e744f5, 0xffd3d3d3), /* lightgrey */
  make_pair(0x28eb3b8c, 0xffffb6c1), /* lightpink */
  make_pair(0x2903623c, 0xffd2691e), /* chocolate */
  make_pair(0x316858a9, 0xffff00ff), /* magenta */
  make_pair(0x31bbd168, 0xffb8860b), /* darkgoldenrod */
  make_pair(0x3256b281, 0xff00fa9a), /* mediumspringgreen */
  make_pair(0x34636c14, 0xff2e8b57), /* seagreen */
  make_pair(0x3507fb41, 0xfffff5ee), /* seashell */
  make_pair(0x39129959, 0xff8a2be2), /* blueviolet */
  make_pair(0x3d8c4edf, 0xffdc143c), /* crimson */
  make_pair(0x3d9dd619, 0xff98fb98), /* palegreen */
  make_pair(0x3e1524a5, 0xff4682b4), /* steelblue */
  make_pair(0x41892743, 0xffff69b4), /* hotpink */
  make_pair(0x4306b960, 0xfff5fffa), /* mintcream */
  make_pair(0x44a8dd73, 0xff6a5acd), /* slateblue */
  make_pair(0x44ab37f8, 0xff708090), /* slategrey */
  make_pair(0x45c1ce55, 0xff1e90ff), /* dodgerblue */
  make_pair(0x46bb5f7e, 0xff7fffd4), /* aquamarine */
  make_pair(0x4cbc0e6b, 0xffffe4e1), /* mistyrose */
  make_pair(0x50632b2a, 0xff20b2aa), /* lightseagreen */
  make_pair(0x5369b689, 0xff3cb371), /* mediumseagreen */
  make_pair(0x55ee0d5b, 0xff8b0000), /* darkred */
  make_pair(0x58bebba3, 0xffff4500), /* orangered */
  make_pair(0x5c293873, 0xff8b008b), /* darkmagenta */
  make_pair(0x5fd898e2, 0xffffefd5), /* papayawhip */
  make_pair(0x607bbc4e, 0xff32cd32), /* limegreen */
  make_pair(0x618d42dd, 0xff6495ed), /* cornflowerblue */
  make_pair(0x61be858a, 0xff8fbc8f), /* darkseagreen */
  make_pair(0x620886da, 0xfff0f8ff), /* aliceblue */
  make_pair(0x628e63dd, 0xffc71585), /* mediumvioletred */
  make_pair(0x634c8b67, 0xff696969), /* dimgrey */
  make_pair(0x67cc74d0, 0xff00008b), /* darkblue */
  make_pair(0x67cd1799, 0xff008b8b), /* darkcyan */
  make_pair(0x67cecf55, 0xff555555), /* darkgrey */
  make_pair(0x68fb7b25, 0xff87cefa), /* lightskyblue */
  make_pair(0x6b6671fe, 0xff556b2f), /* darkolivegreen */
  make_pair(0x6b748956, 0xff7fff00), /* chartreuse */
  make_pair(0x74022737, 0xffafeeee), /* paleturquoise */
  make_pair(0x7880d61e, 0xffdcdcdc), /* gainsboro */
  make_pair(0x7c4d5b99, 0xfffff0f5), /* lavenderblush */
  make_pair(0x7cf2b06b, 0xff00ced1), /* darkturquoise */
  make_pair(0x80da74fb, 0xff87ceeb), /* skyblue */
  make_pair(0x89cea8f9, 0xffdeb887), /* burlywood */
  make_pair(0x920b194d, 0xff006400), /* darkgreen */
  make_pair(0x923edd4c, 0xffbdb76b), /* darkkhaki */
  make_pair(0x93e1b776, 0xffffdab9), /* peachpuff */
  make_pair(0x967dfd4f, 0xff0000cd), /* mediumblue */
  make_pair(0x9e33a98a, 0xff6b8e23), /* olivedrab */
  make_pair(0x9fb78304, 0xffffa07a), /* lightsalmon */
  make_pair(0xa20d484f, 0xffb0c4de), /* lightsteelblue */
  make_pair(0xa89d65b3, 0xffbc8f8f), /* rosybrown */
  make_pair(0xa8a35ba2, 0xff778899), /* lightslategrey */
  make_pair(0xaa2cf10a, 0xffffffe0), /* lightyellow */
  make_pair(0xad388e35, 0xffffe4c4), /* bisque */
  make_pair(0xad5a05c7, 0xffe6e6fa), /* lavender */
  make_pair(0xadd2d33e, 0xfffdf5e6), /* oldlace */
  make_pair(0xafc8858f, 0xffd8bfd8), /* thistle */
  make_pair(0xb3b3bc1e, 0xffdaa520), /* goldenrod */
  make_pair(0xb852b195, 0xfffffaf0), /* floralwhite */
  make_pair(0xb969fed2, 0xff4b0082), /* indigo */
  make_pair(0xbab8a537, 0xffadff2f), /* greenyellow */
  make_pair(0xbcfd2524, 0xffff8c00), /* darkorange */
  make_pair(0xbcfdf799, 0xff9932cc), /* darkorchid */
  make_pair(0xbd58e0b3, 0xff66cdaa), /* mediumaquamarine */
  make_pair(0xbd9413e1, 0xff4169e1), /* royalblue */
  make_pair(0xbf8ca470, 0xff800000), /* maroon */
  make_pair(0xc0ad9f4c, 0xff48d1cc), /* mediumturquoise */
  make_pair(0xc2b0f2bd, 0xff483d8b), /* darkslateblue */
  make_pair(0xc2b34d42, 0xff2f4f4f), /* darkslategrey */
  make_pair(0xc2e5f564, 0xffe9967a), /* darksalmon */
  make_pair(0xc3de262e, 0xffffa500), /* orange */
  make_pair(0xc3def8a3, 0xffda70d6), /* orchid */
  make_pair(0xc5c507bc, 0xff800080), /* purple */
  make_pair(0xc8769375, 0xff9400d3), /* darkviolet */
  make_pair(0xc9c6f66e, 0xfffa8072), /* salmon */
  make_pair(0xca348772, 0xffa0522d), /* sienna */
  make_pair(0xca37d30d, 0xffc0c0c0), /* silver */
  make_pair(0xcc41600a, 0xffff6347), /* tomato */
  make_pair(0xcf57947f, 0xffee82ee), /* violet */
  make_pair(0xd036be93, 0xffb0e0e6), /* powderblue */
  make_pair(0xd086fd06, 0xff228b22), /* forestgreen */
  make_pair(0xd43c6474, 0xffffff00), /* yellow */
  make_pair(0xd5440d16, 0xff00ff7f), /* springgreen */
  make_pair(0xd5796f1a, 0xffcd5c5c), /* indianred */
  make_pair(0xe106b6d7, 0xffff00ff), /* fuchsia */
  make_pair(0xe1b5130f, 0xff9acd32), /* yellowgreen */
  make_pair(0xe4b479fd, 0xfffff8dc), /* cornsilk */
  make_pair(0xe4cacafb, 0xfff0fff0), /* honeydew */
  make_pair(0xe97218a6, 0xffffdead), /* navajowhite */
  make_pair(0xef19e3cb, 0xffb22222), /* firebrick */
  make_pair(0xf3c7ccdb, 0xfff08080), /* lightcoral */
  make_pair(0xf40157ad, 0xff90ee90), /* lightgreen */
  make_pair(0xf456044f, 0xff8b4513), /* saddlebrown */
  make_pair(0xfcad568f, 0xff00bfff), /* deepskyblue */
  make_pair(0xfeea9b21, 0xff40e0d0), /* turquoise */
};

bool compare(const ColorPreset& x, const ColorPreset& y) {
  return x.first < y.first;
}

} // namespace

bool fillColor(const String& cname, Colour* color) {
  auto name = cname.trim().toLowerCase();
  if (name.isEmpty())
    return false;

  uint32 hex;
  if (name[0] == '#' or name.containsOnly("abcdef0123456789")) {
    hex = (uint32) name.getHexValue32();
  } else {
    ColorPreset h((uint32) name.hashCode(), 0);
    auto i = lower_bound(begin(COLOR_PRESETS), end(COLOR_PRESETS), h, compare);
    if (i == end(COLOR_PRESETS) or i->first != h.first)
      return false;
    hex = i->second;
  }
  *color = Colour(hex);
  return true;
}

Colour colorFromInt(uint32 argb) {
  return Colour(argb);
}

}  // namespace echomesh
