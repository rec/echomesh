#!/bin/bash

amixer cset numid=3 1
/usr/bin/python $HOME/echomesh/code/python/Echomesh.py "$*" 2>> /dev/null
