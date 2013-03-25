apt-get update

apt-get install python2.7-dev distcc emacs git libasound2-dev libboost-dev libmad0-dev madplay oss-compat pulseaudio pulseaudio-utils
apt-get install cython python-alsaaudio python-imaging python-pygame python-httplib2 python-setuptools python-pyaudio python-pyalsa

apt-get install locate
apt-get install ffmpeg
sudo apt-get install mpg123

# some missing...


# Install rpi-update!
sudo wget http://goo.gl/1BOfJ -O /usr/bin/rpi-update && sudo chmod +x /usr/bin/rpi-update


# python-scipy

HOSTNAME=Secretary

hostname $HOSTNAME
echo $HOSTNAME > /etc/hostname
sed "s/Chairman/$HOSTNAME/" /etc/hosts > /tmp/hosts # wrong.
mv /tmp/hosts /etc/hosts

cat > /tmp/ssh_config <<EOF
    ClientAliveInterval 30
    TCPKeepAlive yes
    ClientAliveCountMax 99999
EOF

cat /etc/ssh/ssh_config /tmp/ssh_config > /tmp/ssh_config.2
mv /tmp/ssh_config.2 /etc/ssh/ssh_config


mkdir install
cd install

wget http://pypi.python.org/packages/source/s/simplejson/simplejson-2.6.2.tar.gz#md5=9b41cd412dfac7c002aeca61ab0fdfe2
tar xzf simplejson-2.6.2.tar.gz
cd simplejson*
python setup.py install
cd ..

git clone git://github.com/simplegeo/python-oauth2.git
cd python-oauth2
python setup.py install
cd ..

wget http://python-twitter.googlecode.com/files/python-twitter-0.8.2.tar.gz
tar xzf python-twitter-0.8.2.tar.gz
cd python-twitter*
python setup.py install
cd ..

wget http://google-glog.googlecode.com/files/glog-0.3.2.tar.gz
tar xzf glog-0.3.2.tar.gz
cd glog-0.3.2
./configure --prefix=/usr
make && make install
cd ..

wget http://pyyaml.org/download/pyyaml/PyYAML-3.10.tar.gz
tar xzf PyYAML-3.10.tar.gz
cd PyYAML-3.10
python setup.py install
cd ..

wget http://pypi.python.org/packages/source/S/SoundAnalyse/SoundAnalyse-0.1.1.tar.gz#md5=2f51770628d6378bdb8894e91ecce75c
tar xzf SoundAnalyse-0.1.1.tar.gz
cd SoundAnalyse-0.1.1
python setup.py install
cd ..

wget http://pypi.python.org/packages/source/S/SWMixer/SWMixer-0.1.4.tar.gz#md5=3f13db7d8f0371f22b749126680996d1
tar xzf SWMixer-0.1.4.tar.gz
cd SWMixer-0.1.4
python setup.py install
cd ..

wget http://spacepants.org/src/pymad/download/pymad-0.6.tar.gz
tar xzf SWMixer-0.1.4.tar.gz
cd SWMixer-0.1.4
python setup.py install
cd ..

adduser tom # user input!
addgroup tom audio

usermod -g sudo tom

Edit /etc/sudoers:

# Allow members of group sudo to execute any command
# %sudo ALL=(ALL:ALL) ALL
%sudo ALL=NOPASSWD: ALL

modprobe snd_pcm_oss

git config --global credential.helper cache
git config credential.helper 'cache --timeout=3600000'

mkdir echomesh
cd echomesh
git init
git remote add origin https://github.com/rec/echomesh.git
git pull origin master

# Copy .emacs!
# Change /etc/default/keyboard