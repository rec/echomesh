#include "Initialize.h"

namespace echomesh {

namespace {

class EchomeshApplicationBase : public juce::JUCEApplicationBase {
  virtual const String getApplicationName() { return "echomesh"; }

  virtual const String getApplicationVersion() { return "0.0"; }
  virtual bool moreThanOneInstanceAllowed() { return false; }
  virtual void initialise (const String& commandLineParameters) {}
  virtual void shutdown() {}
  virtual void anotherInstanceStarted (const String& commandLine) {}
  virtual void systemRequestedQuit() {}
  virtual void suspended() {}
  virtual void resumed() {}
  virtual void unhandledException (const std::exception*,
                                   const String& sourceFilename,
                                   int lineNumber) {
  }
};

const char* ARGV[] = {"echomesh"};

juce::JUCEApplicationBase* juce_CreateApplication() {
  return new EchomeshApplicationBase();
}

}  // namespace

void initializeJuce() {
  juce::JUCEApplicationBase::createInstance = &juce_CreateApplication;
   juce::JUCEApplicationBase::main(1, ARGV);
}

void shutdownJuce() {
}

}  // namespace echomesh
