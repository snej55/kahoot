#!/usr/bin/bash
echo "Generating binary for $1"

FILE="$(basename -- $1)"

name=$1
IFS='.'
read -ra path <<< "$name"
if [ ! -d "bin/${path[0]}" ]; then
    mkdir bin/${path[0]}
fi

cd bin/${path[0]}
pyinstaller "../../$FILE" --onefile --exclude-module=pygame-ce --icon "../../icon/${path[0]}.ico"