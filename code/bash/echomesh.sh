#!/bin/bash

amixer cset numid=3 1
sudo killall echomesh 2&1 > /dev/null
sudo killall Echomesh.py 2&1 > /dev/null
/usr/bin/python $HOME/echomesh/code/python/Echomesh.py "$*" 2>> /dev/null
