# LOLcoin

LOLcoin is a cryptocurrency built in python. 

## Running the network

```
# Remove old images
docker-compose rm -f

# Build a new image
docker build -t dglass/lolcoin .

# Start the network
docker-compose up
```

## Running just the dnsseeder
The dnsseeder should be the first node you run when starting your network. This server keeps track of all the miner nodes connected to the network and will notify all existing miner nodes when a node is added or removed from the network.

If you start a miner node before the dnsseeder node, the miner node will sit there and try to connect to the dnsseeder node before doing anything else.
```
docker run -p 5001:5001 dglass/lolcoin python dnsseeder.py
```

## Running just the miner

```
docker run -p 5000:5000 dglass/lolcoin python lolcoin.py --dnsseeder_host 172.17.0.2
```

## Posting a transaction to the network
In the example below, 127.0.0.1:5000 is the host and port of a miner on the network
```
curl -X POST -H 'Content-Type: application/json' http://127.0.0.1:5000/txn -d '{"from": "from_address", "to": "to_address", "amount": 99.99}'
```

## Mining a coin
Once some transactions have been posted to the network, you can mine a coin by running the following command. 
```
curl http://127.0.0.1:5000/mine
```
As of now you need to make a request to start the mining process. In the future this will be moved to a cron job that will mine a block on a set interval.