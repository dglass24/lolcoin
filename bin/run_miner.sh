#!/bin/sh

MINERHOST=`python bin/find_ip.py`
MINERPORT=5001

# pull latest image
docker pull dglass/lolcoin

# start the container
docker run -d \
    --env MINERHOST=$MINERHOST \
    --env MINERPORT=$MINERPORT \
    -p $MINERPORT:5000 \
    dglass/lolcoin python lolcoin.py