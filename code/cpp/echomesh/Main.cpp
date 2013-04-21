#include "echomesh/LightingWindow.h"
#include "echomesh/LightReader.h"

class Echomesh  : public JUCEApplication {
 public:
  Echomesh() {}

  const String getApplicationName()       { return ProjectInfo::projectName; }
  const String getApplicationVersion()    { return ProjectInfo::versionString; }
  bool moreThanOneInstanceAllowed()       { return true; }

  void initialise (const String& commandLine) {
    lightingWindow_ = new echomesh::LightingWindow;

    // TODO: we don't store this because it causes an error when it gets
    // deleted at shutdown - so rather have a memory leak!
    readThread_ = new echomesh::LightReader(lightingWindow_->comp_, commandLine);
    readThread_->startThread();
  }

  void shutdown() {
    echomesh::log("shutting down");
    readThread_->signalThreadShouldExit();
    readThread_->waitForThreadToExit(1000);
    readThread_->stopThread(1000);
    lightingWindow_ = nullptr;
  }

  void anotherInstanceStarted (const String& commandLine) {}

 private:
  ScopedPointer<echomesh::LightingWindow> lightingWindow_;
  ScopedPointer<echomesh::LightReader> readThread_;

 private:
  JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(Echomesh)
};

START_JUCE_APPLICATION(Echomesh)
