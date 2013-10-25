#include "echomesh/audio/Player.h"
#include "echomesh/component/LightingWindow.h"
#include "echomesh/network/LightReader.h"

class Echomesh  : public JUCEApplication {
 public:
  Echomesh() {
    echomesh::log("Starting echomesh.");
  }

  const String getApplicationName()       { return ProjectInfo::projectName; }
  const String getApplicationVersion()    { return ProjectInfo::versionString; }
  bool moreThanOneInstanceAllowed()       { return false; }

  void initialise(const String& commandLine) {
    lightingWindow_ = new echomesh::LightingWindow;

    echomesh::log("commandLine: " + commandLine);
    readThread_ = new echomesh::LightReader(lightingWindow_, commandLine,
                                            player_.source());
    readThread_->initialize();
    readThread_->startThread();
  }

  void shutdown() {
    lightingWindow_ = nullptr;
    echomesh::close_log();
  }

  void anotherInstanceStarted(const String& commandLine) {}

 private:
  ScopedPointer<echomesh::LightingWindow> lightingWindow_;
  ScopedPointer<echomesh::LightReader> readThread_;
  echomesh::Player player_;

 private:
  JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(Echomesh)
};

START_JUCE_APPLICATION(Echomesh)
