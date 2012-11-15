#!/bin/bash

HOME=/home/pi/echomesh
LOGS="$HOME/logs"

mkdir -p "$LOGS"

amixer cset numid=3 1
/usr/bin/python "$HOME/python/Echomesh.py" autostart >> "$LOGS/info.log" 2>> "$LOGS/error.log"