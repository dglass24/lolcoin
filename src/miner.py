import datetime as date
import time

from src.blockchain import blockchain
from src.transactions import transactions
from src.network import network
from src.proof_of_work import ProofOfWork
from src.block import Block
from src.logger import logger

MINER_ADDRESS = 'DeZXkR1sTkTUFvBeeovQMahZeEQUbohaof'
MINER_REWARD = 1
BLOCK_TIME_SECONDS = 300 # 5 minutes

class MinerConfig(object):
    JOBS = [
        {
            'id': 'miner',
            'func': 'src.miner:wait_for_new_block',
            'trigger': 'interval',
            'seconds': BLOCK_TIME_SECONDS
        }
    ]

    SCHEDULER_API_ENABLED = True

def wait_for_new_block():
    """
     Miners will boot up on different intervals so if we just ran the mine job each node would start mining on a different
     interval. To fix this we need to check to see if the unix timestamp is divisible by the block time in seconds.
     This way all miners will start mining the new block at the same time.
    """
    waiting_for_new_block = True
    while waiting_for_new_block:
        if int(time.time()) % BLOCK_TIME_SECONDS == 0:
            mine()
        else:
            time.sleep(1)

def mine():
    # get the last proof of work
    last_block = blockchain.get_most_recent_block()
    last_proof = last_block['data']['proof_of_work']

    new_block_index = last_block['index'] + 1
    logger.info('mining new block with height {}'.format(new_block_index))

    # find the new proof of work for the current block being mined
    # The program will hang here until the proof of work is found
    proof = ProofOfWork(last_proof).calculate()

    # once we find a valid proof of work, we know we can mine a block so
    # we reward the miner by adding a transaction
    transactions.add_transaction({
        'from': 'network',
        'to': MINER_ADDRESS,
        'amount': MINER_REWARD
    })

    new_block_data = {
        'proof_of_work': proof,
        'transactions': transactions.get_transactions()
    }

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