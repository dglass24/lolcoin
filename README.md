# LOLcoin

LOLcoin is a cryptocurrency built in python.
 
**<span style="color:red">LOLcoin is still in development. Do not use this in production.</span>**

## Running the dnsseeder
The dnsseeder should be the first node you run when starting your network. This server keeps track of all the miner nodes connected to the network and will notify all existing miner nodes when a node is added or removed from the network.

If you start a miner node before the dnsseeder node, the miner node will sit there and try to connect to the dnsseeder node before doing anything else.
```
docker run -p 5001:5001 dglass/lolcoin python dnsseeder.py
```

## Running the miner

```
docker run -p 5000:5000 dglass/lolcoin python lolcoin.py --dnsseeder_host 172.17.0.2
```

## Posting a transaction to the network
In the example below, 127.0.0.1:5000 is the host and port of a miner on the network
```
curl -X POST -H 'Content-Type: application/json' http://127.0.0.1:5000/txn -d '{"from": "from_address", "to": "to_address", "amount": 99.99}'
```
