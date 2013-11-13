#include "Initialize.h"
#include "Tiny.h"

namespace echomesh {

namespace {

class ApplicationBase : public juce::JUCEApplicationBase {
  virtual const String getApplicationName() { return "echomesh"; }

  virtual const String getApplicationVersion() { return "0.0"; }
  virtual bool moreThanOneInstanceAllowed() { return false; }
  virtual void initialise (const String& commandLineParameters) {
    tiny_.show();
  }
  virtual void shutdown() {
    tiny_.hide();
  }
  virtual void anotherInstanceStarted (const String& commandLine) {}
  virtual void systemRequestedQuit() {}
  virtual void suspended() {}
  virtual void resumed() {}
  virtual void unhandledException (const std::exception*,
                                   const String& sourceFilename,
                                   int lineNumber) {
  }

  Tiny tiny_;
};

const char* ARGV[] = {"echomesh"};

juce::JUCEApplicationBase* juce_CreateApplication() {
  return new ApplicationBase();
}

class ApplicationThread : public Thread {
 public:
  ApplicationThread() : Thread("ApplicationThread") {}

  virtual void run() {
    juce::JUCEApplicationBase::main(1, ARGV);
  }
};

ScopedPointer<ApplicationThread> thread;

}  // namespace

void initializeJuce() {
  juce::JUCEApplicationBase::createInstance = &juce_CreateApplication;
  thread = new ApplicationThread;
  thread->startThread();
}

void shutdownJuce() {
}

}  // namespace echomesh
