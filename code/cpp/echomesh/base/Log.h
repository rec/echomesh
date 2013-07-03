#ifndef __ECHOMESH_LOG__
#define __ECHOMESH_LOG__

namespace echomesh {

void log(const String&, bool newLine = true);
void log2(const String&, bool newLine = true);

void close_log();

}  // namespace echomesh

#endif  // __ECHOMESH_LOG__
