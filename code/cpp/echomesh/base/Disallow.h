#pragma once

#include <stddef.h>

// Macros to disallow various class methods that C++ unfortunately creates
// automatically.  Place either one of these in the private: section of your
// class.

// A macro to disallow the copy constructor and operator= functions.
#define DISALLOW_COPY_AND_ASSIGN(TypeName) \
  TypeName(const TypeName&);               \
  void operator=(const TypeName&)

// A macro to disallow the default constructor, copy constructor and operator=
// functions.
#define DISALLOW_COPY_ASSIGN_AND_EMPTY(TypeName) \
  TypeName();                                    \
  DISALLOW_COPY_AND_ASSIGN(TypeName)

// A macro to disallow the copy constructor and operator= functions.
#define DISALLOW_COPY_ASSIGN_AND_LEAKS(TypeName) \
  DISALLOW_COPY_AND_ASSIGN(TypeName);            \
  JUCE_LEAK_DETECTOR(TypeName)

#define DISALLOW_COPY_ASSIGN_EMPTY_AND_LEAKS(TypeName) \
  DISALLOW_COPY_ASSIGN_AND_EMPTY(TypeName);            \
  JUCE_LEAK_DETECTOR(TypeName)
