#!/bin/sh

IPADDR=`python bin/find_ip.py`
docker run -it dglass/lolcoin python lolcoin.py --seed_host $IPADDR --miner_host $IPADDR