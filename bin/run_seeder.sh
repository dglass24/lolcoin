#!/bin/sh

IPADDR=`python bin/find_ip.py`
python dnsseeder.py --seed_host $IPADDR