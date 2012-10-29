#!/bin/bash

# To execute this from the command line, copy the next line, replace $1 by the
# hostname you'd like to change the machine to, check your work, then paste it
# into a terminal window and press return.

cd ~/echomesh && git pull origin master && ~/echomesh/scripts/change-hostname.sh $1 && sudo shutdown -r now