#ifndef __ECHOMESH__OWNED__
#define __ECHOMESH__OWNED__

#include "Base.h"

namespace echomesh {

class Owned {
 public:
  class Owner;

  Owned() : isOwned_(false) {}
  ~Owned() {}

  // Returns an Owner if you managed to take ownership of this object, or
  // NULL if you didn't.
  Owner* takeOwnership();

 private:
  Mutex mutex_;
  bool isOwned_;

  friend class Owner;
};

class Owned::Owner {
 public:
  ~Owner();

 private:
  explicit Owner(Owned* owned) : owned_(owned) {}
  Owned* owned_;

  friend class Owned;
};

}  // namespace echomesh

#endif  // __ECHOMESH__OWNED__
