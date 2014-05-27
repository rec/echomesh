echo "----------------------"
echo
echo
echo "Running apt-gets (this might take a while)."
echo
echo
echo "----------------------"

apt-get install
 libx11-dev \
 libfreetype6-dev \
 libasound2-dev \
 libxinerama-dev \
 libxcursor-dev \
 python-numpy \
 python2.7-dev \
 python3.4-dev \
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

echo "Raspberry Pi libraries installation completed."
