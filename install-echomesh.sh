#!/bin/bash

PLATFORM=`uname -s | tr '[:upper:]' '[:lower:]'`

SOURCE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

TARGET_DIR=/usr/local/echomesh
TARGET_BIN_DIR=/usr/local/bin
BINARY_DIR=$TARGET_DIR/bin/$PLATFORM
CODE_DIR=$TARGET_DIR/code

BASH_CODE=$CODE_DIR/bash/$PLATFORM

mkdir -p "$TARGET_BIN_DIR"
rm -Rf "$TARGET_DIR"

cp -Rp "$SOURCE_DIR" "$TARGET_DIR"
source "$BASH_CODE"/install-libraries.sh
cp -Rp "$BASH_CODE"/echomesh "$TARGET_BIN_DIR"


echo
echo "echomesh has been installed."
echo "Open a terminal window and type:"
echo
echo "  echomesh"
echo
echo "to start the program."
echo