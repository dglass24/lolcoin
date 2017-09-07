#!/bin/sh

IPADDR=`python bin/find_ip.py`
docker run -d -p 5000:5000 --env SEED_HOST=$IPADDR dglass/lolcoin python dnsseeder.py --seed_host $IPADDR