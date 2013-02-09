#!/bin/bash

HOME=/home/pi/echomesh
LOG="$HOME/log"

mkdir -p "$LOG"

amixer cset numid=3 1
/usr/bin/python "$HOME/code/python/Main.py" "$*" 2>> "$LOG/error.log"