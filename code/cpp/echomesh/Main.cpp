#include "echomesh/Echomesh.h"

class Main  : public JUCEApplication {
 public:
  Main() {}

  void initialise(const String&) { echomesh_.initialise(); }
  void shutdown() { echomesh_.shutdown(); }

  const String getApplicationName()       { return ProjectInfo::projectName; }
  const String getApplicationVersion()    { return ProjectInfo::versionString; }
  bool moreThanOneInstanceAllowed()       { return false; }

  void anotherInstanceStarted(const String& commandLine) {}

 private:
  echomesh::Echomesh echomesh_;

 private:
  JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(Main)
};

START_JUCE_APPLICATION(Main)
