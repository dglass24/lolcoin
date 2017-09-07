import json
import time
import os

from flask import Flask
from flask import request
from flask_apscheduler import APScheduler

from src.block import Block
from src.blockchain import blockchain
from src.network import network
from src.transactions import transactions
from src.config import config
from src.logger import logger
from src.miner import MinerConfig


node = Flask(__name__)

txns = transactions

@node.route('/ping', methods=['GET'])
def get_ping():
    return 'pong\n'

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
    # create var dir if it doesn't exist
    if not os.path.isfile('var/debug.log'):
        open('var/debug.log', 'a').close()

    logger.info('starting up node at {}'.format(config.get_host_url()))

    # register with dnsseeder so other peers can be notified that this node is online
    network.register_with_dnsseeder()

    blockchain.resolve_blockchain()
    blockchain.validate_genesis_block()

    node.config.from_object(MinerConfig())

    scheduler = APScheduler()
    # it is also possible to enable the API directly
    # scheduler.api_enabled = True
    scheduler.init_app(node)
    scheduler.start()

    node.run(threaded=True, host=config.get('miner_host'), port=config.get('miner_port'))

    # deregister with dnsseeder when server is killed
    network.deregister_with_dnsseeder()











