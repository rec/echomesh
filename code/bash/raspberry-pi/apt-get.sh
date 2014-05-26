#!/bin/bash

apt-get -y install\
 clang\
 distcc\
 emacs\
 python-virtualenv\
 rpi-update\
 &&\
\
 python2 -m pip install Pillow &&\
 python3 -m pip install Pillow &&\
\
 pushd /tmp &&\
 rm -Rf /tmp/py-spidev &&\
 git clone git://github.com/doceme/py-spidev &&\
 cd /tmp/py-spidev &&\
 python setup.py install &&\
 popd &&\
 rm -Rf /tmp/py-spidev &&\
\
 apt-get -y update &&\
 apt-get -y upgrade &&\
 rpi-update &&\
 shutdown -r now

