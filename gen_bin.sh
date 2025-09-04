echo "Generating binary for $1"

FILE="$(basename -- $1 .py)"

if [ ! -d "bin/$FILE" ]; then
    mkdir bin/$FILE
fi

echo "bin/$FILE"
cd bin/$FILE
pyinstaller "../../$FILE.py" --onefile --exclude-module=pygame-ce --icon "../../icon/${path[0]}.ico"