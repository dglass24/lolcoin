#!/bin/sh

SEEDHOST=`python bin/find_ip.py`
SEEDPORT=5000

docker run -d \
    --env SEEDHOST=$SEEDHOST \
    --env SEEDPORT=$SEEDPORT \
    -p $SEEDPORT:5000 \
    dglass/lolcoin python dnsseeder.py