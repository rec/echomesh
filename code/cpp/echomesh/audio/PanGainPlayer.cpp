#include "echomesh/audio/PanGainPlayer.h"

namespace echomesh {
namespace audio {

namespace {

static const float EPSILON = 1.0 / 0x10000;

static bool near(float scale, float value) {
  return fabsf(scale - value) < EPSILON;
}

static const float PI = 3.14159265f;
typedef std::pair<float, float> Pan;

static Pan computePan(float p) {
  double theta = jmin(jmax(1.0f + p, 0.0f), 2.0f) * PI / 4.0f;
  return std::make_pair(static_cast<float>(cos(theta)),
                        static_cast<float>(sin(theta)));
}

}  // namespace

void PanGainPlayer::begin() {
  gainPlayer_.begin();
  panPlayer_.begin();
}

void PanGainPlayer::apply(const AudioSourceChannelInfo& info) {
  auto buf = info.buffer;
  if (passthrough_)
    return;

  typedef EnvelopePlayer::SegmentList SegmentList;
  if (gainPlayer_.isConstant()) {
    float value = gainPlayer_.value();
    if (not near(value, 1.0f))
      buf->applyGain(info.startSample, info.numSamples, value);
  } else {
    auto gains = gainPlayer_.getSegments(info.numSamples);
    for (auto& g: gains) {
      buf->applyGainRamp(g.first.time, g.second.time - g.first.time,
                         g.first.value, g.second.value);
    }
  }

  if (panPlayer_.isConstant()) {
    float value = panPlayer_.value();
    if (not near(value, 0.0f)) {
      Pan pan = computePan(value);
      buf->applyGain(0, info.startSample, info.numSamples, pan.first);
      buf->applyGain(1, info.startSample, info.numSamples, pan.second);
    }
  } else {
    float** channels = buf->getArrayOfChannels();
    auto pans = panPlayer_.getSegments(info.numSamples);
    for (auto& p: pans) {
      SampleTime dt = p.second.time - p.first.time;
      float dv = p.second.value - p.first.value;
      auto slope = dv / dt;
      for (SampleTime t = p.first.time; t != p.second.time; ++t)  {
        Pan pan = computePan(p.first.value + slope * (t - p.first.time));
        channels[0][t] *= pan.first;
        channels[1][t] *= pan.second;
      }
    }
  }
}

}  // namespace audio
}  // namespace echomesh
