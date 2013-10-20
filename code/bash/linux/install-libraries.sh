echo "----------------------"
echo
echo
echo "Running apt-gets (this might take a while)."
echo
echo
echo "----------------------"

apt-get install \
 ffmpeg \
 freeglut3-dev \
 git \
 libasound2-dev \
 libfreetype6-dev \
 libfreetype6-dev \
 libjack-dev \
 libjpeg-dev \
 libpng12-dev \
 libx11-dev \
 libxcomposite-dev \
 libxcursor-dev \
 libxinerama-dev \
 locate \
 mesa-common-dev \
 mpg123 \
 oss-compat \
 python-httplib2 \
 python-pip \
 python-pyaudio \
 python-numpy \
 python3-numpy \
 python2.7-dev \
 python3-dev \
 python3-pip \
 python3-setuptools \
 zlib1g-dev \
&&\
\
echo "----------------------" &&\
echo &&\
echo &&\
echo "Installing Pillow." &&\
echo &&\
echo &&\
echo "----------------------" &&\
\
python2 -m pip install Pillow &&\
python3 -m pip install Pillow &&\
\
\
echo "----------------------" &&\
echo &&\
echo &&\
echo "Installing spidev." &&\
echo &&\
echo &&\
echo "----------------------" &&\
\
pushd /tmp &&\
rm -Rf /tmp/py-spidev &&\
git clone git://github.com/doceme/py-spidev &&\
cd /tmp/py-spidev &&\
python setup.py install &&\
popd &&\
rm -Rf /tmp/py-spidev &&\
\
wget http://omxplayer.sconde.net/builds/omxplayer_0.2.6~git20130427~fcfb7911_armhf.deb &&\
dpkg -i omxplayer_0.2.6~git20130427~fcfb7911_armhf.deb &&\
rm omxplayer_0.2.6~git20130427~fcfb7911_armhf.deb &&\
\
echo "Raspberry Pi libraries installation completed."
