#!/bin/sh

MINERHOST=`python bin/find_ip.py`
MINERPORT=5000

docker run -d \
    --env MINERHOST=$MINERHOST \
    --env MINERPORT=$MINERPORT \
    -p $MINERPORT:5000 \
    dglass/lolcoin python lolcoin.py