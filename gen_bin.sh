#!/usr/bin/env bash
if [ ! -d "bin" ]; then
    mkdir bin
fi

if [ ! -d "dist" ]; then
    mkdir dist
else
    rm -rf dist
    mkdir dist
fi

for n in $(seq 1 $#); do
    echo "Generating binary for $1"
    FILE="$(basename -- $1 .py)"

    if [ ! -d "bin/$FILE" ]; then
        mkdir bin/$FILE
    fi

    cd bin/$FILE
    pyinstaller "../../$FILE.py" --onefile --exclude-module=pygame-ce --icon "../../icon/${path[0]}.ico"
    cd ../..

    cp bin/$FILE/dist/$FILE dist

    shift
done

