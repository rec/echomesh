apt-get install\
 ffmpeg\
 git\
 libasound2-dev\
 locate\
 mpg123\
 oss-compat\
 python-httplib2\
 python-imaging\
 python-pyaudio\
 python2.7-dev\
&&\
\
 cd /tmp &&\
 rm -Rf /tmp/py-spidev &&\
 git clone git://github.com/doceme/py-spidev &&\
 cd /tmp/py-spidev &&\
 python setup.py install
