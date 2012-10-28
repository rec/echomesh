#!/bin/bash

HOME=/home/pi/echomesh
LOGS=$HOME/logs

/usr/bin/padsp python $HOME/python/Echomesh.py autostart >> $LOGS/info.log 2>> $LOGS/error.log