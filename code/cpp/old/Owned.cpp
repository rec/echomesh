#include "Owned.h"

#include "Lock.h"

namespace echomesh {

Owned::Owner* Owned::takeOwnership() {
  Lock l(&mutex_);
  if (isOwned_)
    return NULL;
  isOwned_ = true;
  return new Owner(this);
}

Owned::Owner::~Owner() {
  Lock l(&owned_->mutex_);
  owned_->isOwned_ = false;
}

}  // namespace echomesh
