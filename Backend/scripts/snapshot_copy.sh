#!/bin/bash

SOURCE=$1
DEST=$2

mkdir -p "$(dirname "$DEST")"

cp -a "$SOURCE" "$DEST"
