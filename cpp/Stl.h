#ifndef __REC_UTIL_STL__
#define __REC_UTIL_STL__

#include <set>
#include <vector>

#include "Base.h"

namespace echomesh {

template <typename Iterator>
void deletePointers(Iterator begin, Iterator end) {
  for (; begin != end; ++begin)
    delete *begin;
}

template <typename Container>
void deletePointers(Container* c) {
  deletePointers(c->begin(), c->end());
  c->clear();  // TODO: This should move to clear().
}

template <typename Iterator>
void deleteMapPointers(Iterator begin, Iterator end) {
  for (; begin != end; ++begin)
    delete begin->second;
}

template <typename Container>
void deleteMapPointers(Container* c) {
  deleteMapPointers(c->begin(), c->end());
  c->clear();  // TODO:  this should move to clear()
}

template <typename Container>
void clear(Container* c) {
  deletePointers(c);
}

template <typename Container>
void clearMap(Container* c) {
  deleteMapPointers(c);
}

template <typename Container>
typename Container::value_type pop_front(Container *c) {
  typename Container::iterator i = c->begin();
  typename Container::value_type t = *i;
  c->erase(i);
  return t;
}

template <typename Type>
void insert(Type t, std::set<Type>* container) {
  container->insert(t);
}

template <typename Type>
void insert(Type t, std::vector<Type>* container) {
  container->push_back(t);
}

template <typename Type>
std::vector<Type> concat(const std::vector<Type>& x,
                         const std::vector<Type>& y) {
  std::vector<Type> result = x;
  result.insert(result.back(), y.begin(), y.end());

  return result;
}

template <typename Type>
std::set<Type> concat(const std::set<Type>& x, const std::set<Type>& y) {
  std::set<Type> result = x;
  result.insert(y.begin(), y.end());
  return result;
}

}  // namespace echomesh

#endif  // __REC_UTIL_STL__
