#pragma once

#include "echomesh/audio/InputCallback.h"
#include "echomesh/audio/RingBuffer.h"

namespace echomesh {
namespace audio {

class RingCallback {
  public:
    RingCallback(int channels, int size) : buffer_(channels, size) {}
    void callback(int channels, int count, const float** samples) override {
        if (channels != buffer_.channels()) {
            LOG(DFATAL) << "wrong channels: " << channels
                        << " != " << buffer_.channels();
            return;
        }
        buffer_.write(count, samples);
    }

  private:
    RingBuffer buffer_;

    DISALLOW_COPY_ASSIGN_AND_LEAKS(RingCallback);
};

}  // namespace audio
}  // namespace echomesh
