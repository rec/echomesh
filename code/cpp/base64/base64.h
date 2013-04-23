#ifndef __BASE64_BASE64__
#define __BASE64_BASE64__

#include <string>

namespace base64 {

std::string encode(unsigned char const* , unsigned int len);
std::string decode(std::string const& s);

}  // namespace base64

#endif // __BASE64_BASE64__
