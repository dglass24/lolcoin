from .block import Block
from .config import config
from .logger import logger
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

        self.validate_genesis_block()

    def validate_genesis_block(self):
        genesis_block = self.get_genesis_block()
        if genesis_block is None:
            logger.info('No genesis block found. Creating new genesis block.')
            genesis_block = Block(0, str(date.datetime.now()), {'proof_of_work': 9})
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
        # check current block height
        # ping peers to get their block height
        # if current block height is lower, request blocks from peer
        pass

    def write_block_to_disk(self, block, check_height=True):
        # get blockchain filepath from config
        # get last block from blockchain and verify the new block is +1 from current block height
        # serialize block into json (add helper function on block class)
        # append json to end of file
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
            logger.info('Added block {} to blockchain.'.format(block.hash))

    def get_current_block_height(self):
        block = self.get_most_recent_block()
        return block['index']

    def get_most_recent_block(self):
        # Being lazy here. This probably needs to be refactored at some point
        line = subprocess.check_output(['tail', '-1', blockchain_path])
        return json.loads(line)
