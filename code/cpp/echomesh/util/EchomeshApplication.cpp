#include "echomesh/util/EchomeshApplication.h"

namespace echomesh {

namespace {

VoidCaller CALLBACK;
void* USER_DATA;

class Quitter : public CallbackMessage {
  virtual void messageCallback() {
    JUCEApplicationBase::quit();
  }
};

class ApplicationBase : public juce::JUCEApplicationBase {
 public:
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

void startApplication(VoidCaller cb, void* userData) {
  CALLBACK = cb;
  USER_DATA = userData;
  juce::JUCEApplicationBase::createInstance = &juce_CreateApplication;
  juce::JUCEApplicationBase::main(1, ARGV);
}

void stopApplication() {
  // DLOG(INFO) << "Quitting juce";
  (new Quitter)->post();
}

}  // namespace echomesh
