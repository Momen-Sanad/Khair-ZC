#!/bin/bash

install_windows() {
    echo "Detected Windows. Installing dependencies..."
    cd client || exit
    npm install

    cd ../server || exit
    pip install -r requirements.txt
}

install_linux() {
    echo "Detected Linux. Installing dependencies..."
    cd client || exit
    npm install

    cd ../server || exit
    pip install -r requirements.txt
}

case "$(uname -s)" in
    Darwin)
        echo "Detected macOS. Installing dependencies..."
        install_linux
        ;;
    Linux)
        install_linux
        ;;
    CYGWIN*|MINGW32*|MSYS*|MINGW*)
        install_windows
        ;;
    *)
        echo "Unsupported OS"
        exit 1
        ;;
esac

echo "Installation complete."
