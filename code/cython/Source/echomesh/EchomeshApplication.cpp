#include "JuceHeader.h"

#include "echomesh/EchomeshApplication.h"

namespace echomesh {

namespace {

class ApplicationBase : public juce::JUCEApplicationBase {
  virtual const String getApplicationName() { return "echomesh"; }
  virtual const String getApplicationVersion() { return "0.0"; }
  virtual bool moreThanOneInstanceAllowed() { return false; }
  virtual void initialise(const String&) {}
  virtual void shutdown() {}
  virtual void anotherInstanceStarted(const String&) {}
  virtual void systemRequestedQuit() {
    stopEchomesh();
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

void startEchomesh() {
  juce::JUCEApplicationBase::createInstance = &juce_CreateApplication;
  juce::JUCEApplicationBase::main(1, ARGV);
}

void stopEchomesh() {
  juce::JUCEApplicationBase::quit();
}

}  // namespace echomesh
