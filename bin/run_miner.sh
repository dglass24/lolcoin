#!/bin/sh

IPADDR=`python bin/find_ip.py`
python lolcoin.py --seed_host $IPADDR --miner_host $IPADDR