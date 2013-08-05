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
 libjack-dev \
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
 python2.7-dev \
 python3-dev \
 python3-setuptools \
 python3-pip \
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
pip install Pillow &&\
pip-3.2 install Pillow &&\
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
