#!/bin/bash

hostname $1
echo $1 > /etc/hostname
sed "s/Chairman/$1/" /etc/hosts > /tmp/hosts
mv /tmp/hosts /etc/hosts

echo "Hostname change to $1"
cat /etc/hosts