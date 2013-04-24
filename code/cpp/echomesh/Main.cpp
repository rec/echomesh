#include "echomesh/LightingWindow.h"
#include "echomesh/LightReader.h"

class Echomesh  : public JUCEApplication {
 public:
  Echomesh() {}

  const String getApplicationName()       { return ProjectInfo::projectName; }
  const String getApplicationVersion()    { return ProjectInfo::versionString; }
  bool moreThanOneInstanceAllowed()       { return false; }

  void initialise(const String& commandLine) {
    lightingWindow_ = new echomesh::LightingWindow;

    readThread_ = new echomesh::LightReader(lightingWindow_->comp_, commandLine);
    readThread_->startThread();
  }

  void shutdown() {
    std::cerr << "Shutting down\n";
    std::cerr.flush();
    echomesh::log("shutting down");
    readThread_->kill();
    lightingWindow_ = nullptr;
    echomesh::close_log();
  }

  void anotherInstanceStarted(const String& commandLine) {}

 private:
  ScopedPointer<echomesh::LightingWindow> lightingWindow_;
  ScopedPointer<echomesh::LightReader> readThread_;

 private:
  JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(Echomesh)
};

START_JUCE_APPLICATION(Echomesh)
