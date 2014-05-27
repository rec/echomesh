#CXXFLAGS="-arch x86_64 -O2 -std=c++11 -stdlib=libc++"
CXXFLAGS="-arch x86_64 -O2"
_DIRECTORY=`pwd`/build
pushd glog

./configure --enable-static=yes --enable-shared=no CXX=clang++ CXXFLAGS="$CXXFLAGS" --prefix=$_DIRECTORY\
 && make && make install

popd
