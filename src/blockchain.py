from block import Block
import datetime as date

class Blockchain:
    def __init__(self):
        self.blockchain = [self.create_genesis_block()]

    def create_genesis_block(self):
        # manually construct block with index zero with random previous hash
        return Block(0, date.datetime.now(), {'proof_of_work': 23,'transactions': []}, '0')

    def next_block(self, last_block):
        index = last_block.index + 1
        timestamp = date.datetime.now()
        data = {'transactions': []}
        last_hash = last_block.hash
        return Block(index, timestamp, data, last_hash)

    def set(self, blockchain_dict):
        self.blockchain = []
        for block_dict in blockchain_dict:
            self.blockchain.append(
                Block(block_dict['index'],
                      block_dict['timestamp'],
                      block_dict['data'],
                      None,
                      block_dict['hash']
                      )
            )

        print self.blockchain