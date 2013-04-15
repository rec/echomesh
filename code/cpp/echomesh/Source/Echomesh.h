#ifndef __ECHOMESH__
#define __ECHOMESH__

#include <stdio.h>

#include <iostream>
#include <string>
#include <vector>

#include "../JuceLibraryCode/JuceHeader.h"
#include "disallow.h"

using std::string;
using std::vector;

namespace echomesh {

void log(const string&);
void close_log();

}

#endif  // __ECHOMESH__
