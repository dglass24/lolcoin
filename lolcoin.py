import datetime as date
import json

from flask import Flask
from flask import request

from src.block import Block
from src.blockchain import Blockchain
from src.proof_of_work import ProofOfWork

node = Flask(__name__)

blockchain = Blockchain()

##### SERVER #####

peer_nodes = []
transactions = []
miner_address = 'f38c966908390d7fdffcbbb44b8e0439aa34fd71f1cbdec1cc7d4eecf19515f7'

def broadcast_new_block():
    for node_url in peer_nodes:
        request.get(node_url + '/blocks').content

def find_new_chains():
    # retrieve blockchains from each peer node
    other_chains = []
    for node_url in peer_nodes:
        peer_blockchain = request.get(node_url + '/blocks').content
        peer_blockchain = json.loads(peer_blockchain)
        other_chains.append(peer_blockchain)
    return other_chains

def consensus():
    global blockchain

    # Get blockchains from other peers
    other_blockchains = find_new_chains()

    # If our chain isn't the longest then we store the longest chain
    longest = blockchain
    for chain in other_blockchains:
        if len(chain) > len(blockchain.blockchain):
            longest = chain
    blockchain.blockchain = longest

@node.route('/txn', methods=['POST'])
def transaction():
    if request.method == 'POST':
        global transactions
        new_txn = request.get_json()
        transactions.append(new_txn)
        print 'New transaction'
        print 'FROM: {}'.format(new_txn['from'])
        print 'TO: {}'.format(new_txn['to'])
        print 'AMOUNT: {}'.format(new_txn['amount'])
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

    return json.dumps({
        'index': new_block.index,
        'timestamp': str(new_block.timestamp),
        'data': new_block.data,
        'hash': new_block.hash,
    })

@node.route('/blocks', methods=['GET'])
def blocks():
    # the blockchain is a list of Block objects. Convert the blockchain to a list of dictionaries
    # so we can serialize the blockchain to json
    blockchain_list = []
    for block in blockchain.blockchain:
        blockchain_list.append({
            'index': block.index,
            'timestamp': str(block.timestamp),
            'data': block.data,
            'hash': block.hash
        })
    return json.dumps(blockchain_list)

node.run()











