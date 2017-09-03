from .block import Block
from .config import config
from .logger import logger
from .network import network
import datetime as date
import subprocess
import json
import os.path

blockchain_path = config.get('blockchain_path')

class Blockchain:
    def __init__(self):
        # create blockchain file if it does not exist
        if not os.path.isfile(blockchain_path):
            open(blockchain_path, 'a').close()

    def validate_genesis_block(self):
        genesis_block = self.get_genesis_block()
        if genesis_block is None:
            logger.info('No genesis block found. Creating new genesis block.')
            genesis_block = Block(1, str(date.datetime.now()), {'proof_of_work': 9})
            genesis_block.hash_block("dummy_previous_hash")
            self.write_block_to_disk(genesis_block, check_height=False)

    def get_genesis_block(self):
        try:
            with open(blockchain_path, 'r') as f:
                genesis_block = json.loads(f.readline())
        except:
            genesis_block = None
        return genesis_block

    def resolve_blockchain(self):
        if len(network.get_nodes()) == 0:
            return

        # ping peers to get their block height
        max_block_height, max_block_height_peer = network.get_max_block_height()
        logger.info('max block height = {}'.format(max_block_height))

        # Download blockchain from peer if max block height of a peer is greater than current block height on this node
        current_block_height = self.get_current_block_height()
        if current_block_height is None or current_block_height < max_block_height:
            network.download_blockchain_from_peer(current_block_height, max_block_height, max_block_height_peer)

    def write_block_to_disk(self, block, check_height=True):
        if check_height:
            current_height = self.get_current_block_height()
            if check_height and block.index != current_height + 1:
                logger.info('Could not write block to blockchain. New block height is not current block height + 1.')
                return

        if block.hash is None:
            logger.info('Could not write block to blockchain. Block does not contain hash.')
            return

        blockchain_file = config.get('blockchain_path')
        with open(blockchain_file, "a") as fp:
            fp.write('{}\n'.format(json.dumps(block.__dict__)))
            logger.info('Added block={} height={} to blockchain.'.format(block.hash, block.index))

    def get_current_block_height(self):
        block = self.get_most_recent_block()
        if block:
            return block['index']
        else:
            return None

    def get_most_recent_block(self):
        # Being lazy here. This probably needs to be refactored at some point
        line = subprocess.check_output(['tail', '-1', blockchain_path])
        if line:
            return json.loads(line)
        else:
            return None

    def get_block_by_height(self, height):
        with open(blockchain_path, "r") as text_file:
            lines = text_file.readlines()
            line = lines[height].strip()
            return line

blockchain = Blockchain()