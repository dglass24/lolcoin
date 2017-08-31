from block import Block
import datetime as date

#### BLOCK ####

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