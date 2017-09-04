import datetime as date

from src.blockchain import blockchain
from src.transactions import transactions
from src.network import network
from src.proof_of_work import ProofOfWork
from src.block import Block

miner_address = 'f38c966908390d7fdffcbbb44b8e0439aa34fd71f1cbdec1cc7d4eecf19515f7'

class MinerConfig(object):
    JOBS = [
        {
            'id': 'miner',
            'func': 'src.miner:mine',
            'trigger': 'interval',
            'seconds': 10
        }
    ]

    SCHEDULER_API_ENABLED = True

def mine():
    # get the last proof of work
    last_block = blockchain.get_most_recent_block()
    last_proof = last_block['data']['proof_of_work']

    # find the new proof of work for the current block being mined
    # The program will hang here until the proof of work is found
    proof = ProofOfWork(last_proof).calculate()

    # once we find a valid proof of work, we know we can mine a block so
    # we reward the miner by adding a transaction
    transactions.add_transaction({
        'from': 'network',
        'to': miner_address,
        'amount': 1
    })

    new_block_data = {
        'proof_of_work': proof,
        'transactions': transactions.get_transactions()
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
    transactions.clear_transactions()

    # notify all nodes in network of new block
    network.broadcast_new_block(new_block)