import datetime as date
import json

from flask import Flask
from flask import request

from src.block import Block
from src.blockchain import blockchain
from src.network import network
from src.transactions import transactions
from src.proof_of_work import ProofOfWork
from src.config import config
from src.logger import logger

node = Flask(__name__)

miner_address = 'f38c966908390d7fdffcbbb44b8e0439aa34fd71f1cbdec1cc7d4eecf19515f7'

@node.route('/ping', methods=['GET'])
def get_ping():
    return 'pong\n'

@node.route('/mine', methods=['GET'])
def mine():
    # get the last proof of work
    last_block = blockchain.get_most_recent_block()
    last_proof = last_block['data']['proof_of_work']

    # find the new proof of work for the current block being mined
    # The program will hang here until the proof of work is found
    proof = ProofOfWork(last_proof).calculate()

    # once we find a valid proof of work, we know we can mine a block so
    # we reward the miner by adding a transaction
    txns.add_transaction({
        'from': 'network',
        'to': miner_address,
        'amount': 1
    })

    new_block_data = {
        'proof_of_work': proof,
        'transactions': txns.get_transactions()
    }
    new_block_index = last_block['index'] + 1
    new_block_timestamp = str(date.datetime.now())
    last_block_hash = last_block['hash']

    # create the new block
    new_block = Block(
        new_block_index,
        new_block_timestamp,
        new_block_data
    )
    new_block.hash_block(last_block_hash)

    blockchain.write_block_to_disk(new_block)
    txns.clear_transactions()

    # notify all nodes in network of new block
    network.broadcast_new_block(new_block)

    return json.dumps({
        'index': new_block.index,
        'timestamp': str(new_block.timestamp),
        'data': new_block.data,
        'hash': new_block.hash,
    })

@node.route('/addtxn', methods=['POST'])
def post_add_transaction():
    if request.method == 'POST':
        new_txn = request.get_json()
        txns.add_transaction(new_txn)
        network.broadcast_new_transaction(new_txn)
        return 'Transaction submission success\n'

@node.route('/receivetxn', methods=['POST'])
def post_receive_transaction():
    if request.method == 'POST':
        new_txn = request.get_json()
        txns.add_transaction(new_txn)
        return 'ok'

@node.route('/blockheight', methods=['GET'])
def get_blockheight():
    return str(blockchain.get_current_block_height())

@node.route('/newblock', methods=['POST'])
def post_newblock():
    if request.method == 'POST':
        data = json.loads(request.get_json(force=True))
        logger.info('Received new block from {}'.format(request.remote_addr))

        # load block object from json data
        new_block = Block(
            data['index'],
            data['timestamp'],
            data['data'],
            data['hash']
        )

        blockchain.write_block_to_disk(new_block)
        txns.clear_transactions()
    return 'ok'

@node.route('/getblock', methods=['POST'])
def post_getblocks():
    if request.method == 'POST':
        data = json.loads(request.get_json())
        block_height = data['height']
        block = blockchain.get_block_by_height(block_height)
        return block

@node.route('/addhost', methods=['POST'])
def post_addhost():
    if request.method == 'POST':
        data = json.loads(request.get_json(force=True))
        logger.info('received new node from dnsseeder')
        network.add_node(data['host'])
    return 'ok'

@node.route('/removehost', methods=['POST'])
def post_removehost():
    if request.method == 'POST':
        data = json.loads(request.get_json(force=True))
        network.remove_node(data['host'])
    return 'ok'

if __name__ == '__main__':
    logger.info('starting up node at {}'.format(config.get_host_url()))

    # register with dnsseeder so other peers can be notified that this node is online
    network.register_with_dnsseeder()

    blockchain.resolve_blockchain()
    blockchain.validate_genesis_block()

    txns = transactions

    node.run(host=config.get('host'), port=config.get('port'))

    # deregister with dnsseeder when server is killed
    network.deregister_with_dnsseeder()











