#!/bin/sh

IPADDR=`python bin/find_ip.py`
docker run -it dglass/lolcoin python dnsseeder.py --seed_host $IPADDR