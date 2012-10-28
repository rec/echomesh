#!/bin/bash

HOME=~/echomesh
LOGS="$HOME/logs"

mkdir -p "$LOGS"

/usr/bin/padsp python "$HOME/python/Echomesh.py" autostart >> "$LOGS/info.log" 2>> "$LOGS/error.log"