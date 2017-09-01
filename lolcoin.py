import datetime as date
import requests
import json

from flask import Flask
from flask import request

from src.block import Block
from src.blockchain import Blockchain
from src.network import Network
from src.proof_of_work import ProofOfWork
from src.config import Config

node = Flask(__name__)

config = Config()

# TODO: Download blockchain on initial startup and store on disk
blockchain = Blockchain()

# TODO: Add dnsseed to automatically discover all peers in network
network = Network()

transactions = []
miner_address = 'f38c966908390d7fdffcbbb44b8e0439aa34fd71f1cbdec1cc7d4eecf19515f7'

@node.route('/txn', methods=['POST'])
def transaction():
    if request.method == 'POST':
        global transactions
        new_txn = request.get_json()
        transactions.append(new_txn)
        return 'Transaction submission success\n'

@node.route('/mine', methods=['GET'])
def mine():
    global transactions

    # get the last proof of work
    last_block = blockchain.blockchain[len(blockchain.blockchain) - 1]
    last_proof = last_block.data['proof_of_work']

    # find the new proof of work for the current block being mined
    # The program will hang here until the proof of work is found
    proof = ProofOfWork(last_proof).calculate()

    # once we find a valid proof of work, we know we can mine a block so
    # we reward the miner by adding a transaction
    transactions.append({
        'from': 'network',
        'to': miner_address,
        'amount': 1
    })

    new_block_data = {
        'proof_of_work': proof,
        'transactions': list(transactions)
    }
    new_block_index = last_block.index + 1
    new_block_timestamp = date.datetime.now()
    last_block_hash = last_block.hash

    # create the new block
    new_block = Block(
        new_block_index,
        new_block_timestamp,
        new_block_data,
        last_block_hash
    )

    # once we have a block we can clear the transactions
    transactions = []

    blockchain.blockchain.append(new_block)

    # notify all nodes in network of new block
    network.broadcast(blockchain.blockchain)

    return json.dumps({
        'index': new_block.index,
        'timestamp': str(new_block.timestamp),
        'data': new_block.data,
        'hash': new_block.hash,
    })

@node.route('/blockchainupdate', methods=['POST'])
def post_newblock():
    if request.method == 'POST':
        print '*** blockchain update'
        data = json.loads(request.get_json(force=True))
        blockchain.set(data)
    return 'ok'

@node.route('/addhost', methods=['POST'])
def post_addhost():
    if request.method == 'POST':
        data = json.loads(request.get_json(force=True))
        network.add_node(data['host'])
    return 'ok'

if __name__ == '__main__':
    network.register_with_dnsseeder()
    node.run(host=config.get('host'), port=config.get('port'))











