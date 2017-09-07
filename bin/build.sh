#!/bin/sh

if [ `dirname $0` == '.' ]
    then
    echo "Build script must be run from root directory, not bin directory"
    exit 0
fi

docker build -t dglass/lolcoin .