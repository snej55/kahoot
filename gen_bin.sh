#!/usr/bin/env bash
if [ ! -d "bin" ]; then
    mkdir bin
fi

arch="$(uname -m)"
os="$OSTYPE"
dest=kahoot-$os-$arch
if [ ! -d "$dest" ]; then
    mkdir $dest
else
    rm -rf $dest
    mkdir $dest
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

    cp bin/$FILE/dist/$FILE $dest

    shift
done
rm -rf bin

cp ./LICENSE $dest
cp ./GUIDE.md $dest
