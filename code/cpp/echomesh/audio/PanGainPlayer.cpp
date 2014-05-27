#include "echomesh/audio/PanGainPlayer.h"

namespace echomesh {
namespace audio {

namespace {

static const float PI = 3.14159265f;
typedef std::pair<float, float> Pan;

static Pan computePan(float p) {
  auto theta = jmin(jmax(1.0f + p, 0.0f), 2.0f) * PI / 4.0f;
  return std::make_pair(static_cast<float>(cos(theta)),
                        static_cast<float>(sin(theta)));
}

}  // namespace

PanGainPlayer::PanGainPlayer(Envelope* gain, Envelope* pan) {
  if (gain) {
    if (gain->isConstant and near(gain->value, 1.0f))
      delete gain;
    else
      gainPlayer_ = make_unique<EnvelopePlayer>(gain);
  }

  if (pan) {
    if (pan->isConstant and near(pan->value, 0.0f))
      delete pan;
    else
      panPlayer_ = make_unique<EnvelopePlayer>(pan);
  }
}

void PanGainPlayer::begin() {
  if (gainPlayer_.get())
    gainPlayer_->begin();

  if (panPlayer_.get())
    panPlayer_->begin();
}

void PanGainPlayer::apply(const AudioSourceChannelInfo& info) {
  if (gainPlayer_.get())
    applyGain(info);

  if (panPlayer_.get())
    applyPan(info);
}

void PanGainPlayer::applyGain(const AudioSourceChannelInfo& info) {
  if (gainPlayer_->isConstant()) {
    auto value = gainPlayer_->value();
    info.buffer->applyGain(info.startSample, info.numSamples, value);

  } else {
    auto gains = gainPlayer_->getSegments(info.numSamples);
    for (auto& g: gains) {
      info.buffer->applyGainRamp(g.first.time, g.second.time - g.first.time,
                                 g.first.value, g.second.value);
    }
  }
}

void PanGainPlayer::applyPan(const AudioSourceChannelInfo& info) {
  if (panPlayer_->isConstant()) {
    auto pan = computePan(panPlayer_->value());
    info.buffer->applyGain(0, info.startSample, info.numSamples, pan.first);
    info.buffer->applyGain(1, info.startSample, info.numSamples, pan.second);

  } else {
    auto** channels = info.buffer->getArrayOfWritePointers();
    auto pans = panPlayer_->getSegments(info.numSamples);

    for (auto& p: pans) {
      auto dt = p.second.time - p.first.time;
      auto dv = p.second.value - p.first.value;
      auto slope = dv / dt;
      for (SampleTime t = p.first.time; t != p.second.time; ++t)  {
        auto pan = computePan(p.first.value + slope * (t - p.first.time));
        channels[0][t] *= pan.first;
        channels[1][t] *= pan.second;
      }
    }
  }
}

}  // namespace audio
}  // namespace echomesh
