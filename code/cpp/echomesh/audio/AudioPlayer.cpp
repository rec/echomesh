#include <unordered_map>

#include "echomesh/audio/AudioPlayer.h"
#include "echomesh/audio/DefaultDevice.h"

namespace echomesh {
namespace audio {

static std::unordered_map<string, unique_ptr<AudioPlayer>> PLAYERS;

AudioPlayer::AudioPlayer(const string& name, int channels)
    : name_(name),
      channels_(channels),
      sourceCount_(0) {
  error_ = manager_.initialise(0, channels, nullptr, false, name);
  if (error_.length()) {
    LOG(ERROR) << error_.toStdString();
  } else {
    player_.setSource(&mixer_);
    manager_.addAudioCallback(&player_);
  }
}

AudioPlayer::~AudioPlayer() {
  manager_.removeAudioCallback(&player_);
  player_.setSource(nullptr);
}

AudioPlayer* AudioPlayer::getPlayer(const string& name, int channels) {
  string n = name.empty() ? defaultOutputDevice() : name;
  auto i = PLAYERS.find(n);
  if (i != PLAYERS.end())
    return i->second.get();

  unique_ptr<AudioPlayer> player(new AudioPlayer(n, channels));
  AudioPlayer* p = player.get();
  PLAYERS.insert(i, std::make_pair(n, std::move(player)));
  return p;
}

void AudioPlayer::addInputSource(AudioSource* source) {
  mixer_.addInputSource(source, false);
  ++sourceCount_;
}

bool AudioPlayer::removeInputSource(AudioSource* source) {
  mixer_.removeInputSource(source);
  if (true)
    return not --sourceCount_;

  if (not --sourceCount_) {
    if (not PLAYERS.erase(name_))
      LOG(DFATAL) << "Didn't erase Player " << name_;
  }
}

void AudioPlayer::removePlayer(AudioPlayer* player) {
  string name = player->name_;
  if (not PLAYERS.erase(name))
    LOG(DFATAL) << "Didn't erase Player " << name;
}

}  // namespace audio
}  // namespace echomesh
