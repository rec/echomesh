#ifndef __REC_UTIL_LISTENER_LISTENER__
#define __REC_UTIL_LISTENER_LISTENER__

#include <map>
#include <set>

#include "rec/util/Deletable.h"
#include "rec/util/HasLock.h"

namespace rec {
namespace util {

typedef juce::ScopedLock Lock;

template <typename Type> class Broadcaster;

template <typename Type>
class Listener : public HasLock, public Deletable {
 public:
  typedef std::set<Broadcaster<Type>*> BroadcasterSet;
  typedef typename BroadcasterSet::iterator iterator;

  Listener() {}
  virtual ~Listener();

  virtual void operator()(Type x) = 0;

 private:
  CriticalSection lock_;

  virtual void wasRemovedFrom(Broadcaster<Type>*);
  void wasAddedTo(Broadcaster<Type>*);

  BroadcasterSet broadcasters_;

  DISALLOW_COPY_AND_ASSIGN(Listener);
  JUCE_LEAK_DETECTOR(Listener<Type>);

  friend class Broadcaster<Type>;
};

//
// Broadcast updates of type Type to a set of Listener<Type>.
//
template <typename Type>
class Broadcaster : public Deletable {
 public:
  typedef std::set<Listener<Type>*> ListenerSet;
  typedef typename ListenerSet::iterator iterator;

  Broadcaster() {}

  virtual ~Broadcaster();

  virtual void broadcast(Type x);

  virtual void addListener(Listener<Type>* listener);
  virtual void removeListener(Listener<Type>* listener);

  // int listenerSize() const { Lock l(lock_); return listeners_.size(); }

 private:
  CriticalSection lock_;
  ListenerSet listeners_;

  DISALLOW_COPY_AND_ASSIGN(Broadcaster);
  JUCE_LEAK_DETECTOR(Broadcaster<Type>);
};

template <typename Type>
Listener<Type>::~Listener() {
  BroadcasterSet toDelete;
  {
    Lock l(lock_);
    if (broadcasters_.empty())
      return;

    broadcasters_.swap(toDelete);
  }

  for (iterator i = toDelete.begin(); i != toDelete.end(); ++i)
    (*i)->removeListener(this);
}

template <typename Type>
void Listener<Type>::wasRemovedFrom(Broadcaster<Type>* broadcaster) {
  Lock l(lock_);
  broadcasters_.erase(broadcaster);
}

template <typename Type>
void Listener<Type>::wasAddedTo(Broadcaster<Type>* broadcaster) {
  Lock l(lock_);
  broadcasters_.insert(broadcaster);
}

template <typename Type>
void Broadcaster<Type>::broadcast(Type x) {
  Lock l(lock_);
  for (iterator i = listeners_.begin(); i != listeners_.end(); ++i) {
    Listener<Type>* listener = *i;
    Lock m(listener->lock_);
    (*listener)(x);
  }
}

template <typename Type>
Broadcaster<Type>::~Broadcaster() {
  Lock l(lock_);
  for (iterator i = listeners_.begin(); i != listeners_.end(); ++i)
    (*i)->wasRemovedFrom(this);
}

template <typename Type>
void Broadcaster<Type>::addListener(Listener<Type>* listener) {
  {
    Lock l(lock_);
    listeners_.insert(listener);
  }

  listener->wasAddedTo(this);
}

template <typename Type>
void Broadcaster<Type>::removeListener(Listener<Type>* listener) {
  {
    Lock l(lock_);
    listeners_.erase(listener);
  }

  listener->wasRemovedFrom(this);
}

}  // namespace util
}  // namespace rec

#endif  // __REC_UTIL_LISTENER_LISTENER__
