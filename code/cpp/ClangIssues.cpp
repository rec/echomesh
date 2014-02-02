#include <functional>

typedef std::function<float(float)> FloatFunction;

float composer(FloatFunction f, FloatFunction g, float x) {
  return f(g(x));
}

FloatFunction compose1(FloatFunction f, FloatFunction g) {
  return std::bind(composer, f, g);
}

FloatFunction compose2(FloatFunction f, FloatFunction g) {
  return std::bind(composer, f, g, std::placeholders::_3);
}

FloatFunction compose3(FloatFunction f, FloatFunction g) {
  return [&](float x) { return f(g(x)); };
}

