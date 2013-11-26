#include "echomesh/util/EchomeshApplication.h"

namespace echomesh {

namespace {

AppCallback CALLBACK;
void* USER_DATA;

class ApplicationBase : public juce::JUCEApplicationBase {
  virtual const String getApplicationName() { return "echomesh"; }
  virtual const String getApplicationVersion() { return "0.0"; }
  virtual bool moreThanOneInstanceAllowed() { return false; }
  virtual void initialise(const String&) {
    if (CALLBACK and USER_DATA)
      CALLBACK(USER_DATA);
  }
  virtual void shutdown() {}
  virtual void anotherInstanceStarted(const String&) {}
  virtual void systemRequestedQuit() {
    stopApplication();
  }
  virtual void suspended() {}
  virtual void resumed() {}
  virtual void unhandledException(
      const std::exception*, const String& sourceFilename, int lineNumber) {
  }

};

const char* ARGV[] = {"echomesh"};

juce::JUCEApplicationBase* juce_CreateApplication() {
  return new ApplicationBase();
}

}  // namespace

void startApplication(AppCallback cb, void* userData) {
  CALLBACK = cb;
  USER_DATA = userData;
  juce::JUCEApplicationBase::createInstance = &juce_CreateApplication;
  juce::JUCEApplicationBase::main(1, ARGV);
}

void stopApplication() {
  DLOG(INFO) << "Quitting juce";
  juce::JUCEApplicationBase::quit();
}

}  // namespace echomesh
