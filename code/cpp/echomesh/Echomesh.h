#ifndef __ECHOMESH_ECHOMESH__
#define __ECHOMESH_ECHOMESH__

#include "JuceLibraryCode/JuceHeader.h"

namespace echomesh {

class Echomesh {
 public:
  Echomesh();
  ~Echomesh();

  void initialise();
  void shutdown();

  class Impl;

 private:
  ScopedPointer<Impl> impl_;

  JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(Echomesh);
};

}  // namespace echomesh

#endif  // __ECHOMESH_ECHOMESH__
