from .config import config
from .block import Block
from .logger import logger
import http
import json
import time

class Network:
    def __init__(self):
        self.peer_nodes = set()

    def get_nodes(self):
        return self.peer_nodes

    def add_nodes(self, peers):
        logger.info('adding peer nodes')
        for peer in peers:
            self.add_node(peer)
        logger.info('done adding peer nodes')

    def add_node(self, node):
        if node not in self.peer_nodes:
            self.peer_nodes.add(node)
            logger.info('added peer node {}'.format(node))

    def remove_node(self, node):
        if node in self.peer_nodes:
            self.peer_nodes.remove(node)
            logger.info('removed peer node {}'.format(node))

    def broadcast_new_block(self, new_block):
        for node in self.get_nodes():
            http.post('http://{}/newblock'.format(node), new_block.to_json())

    def broadcast_new_transaction(self, new_txn):
        for node in self.get_nodes():
            http.post('http://{}/receivetxn'.format(node), new_txn)

    def get_max_block_height(self):
        """
        Returns the maximum block height from all peers on the network
        """
        max_height = 0
        max_height_node = None

        for node in self.get_nodes():
            block_height = http.get('http://{}/blockheight'.format(node))
            max_height = max(max_height, int(block_height))

            if max_height == int(block_height):
                max_height_node = node

        return max_height, max_height_node

    def download_blockchain_from_peer(self, current_height, max_height, peer):
        if current_height is None:
            current_height = 0
            for i in range(current_height, max_height):
                url = 'http://{}/getblock'.format(peer)
                data = http.post(url, {"height": i})
                data = json.loads(data)

                # load block object from json data
                new_block = Block(
                    data['index'],
                    data['timestamp'],
                    data['data'],
                    data['hash']
                )

                from .blockchain import blockchain
                blockchain.write_block_to_disk(new_block, False)

    def register_with_dnsseeder(self):
        registered = False

        while not registered:
            register_url = '{}/register'.format(config.get_dnsseeder_url())
            logger.info('trying to connect to dnsseeder at {}'.format(register_url))

            try:
                peers = http.post(register_url, {'port': config.get('seed_port')})
                peers = json.loads(peers)
                registered = True
            except Exception, e:
                logger.error('error: '+ repr(e))
                logger.info('could not connect to dnsseeder, retrying in 30 seconds')
                time.sleep(30)


        logger.info('registered with dnsseeder')
        logger.info('received {} peer nodes from dnsseeder'.format(len(peers)))

        if len(peers) == 0:
            return

        self.add_nodes(peers)

    def deregister_with_dnsseeder(self):
        deregister_url = '{}/deregister'.format(config.get_dnsseeder_url())
        logger.info('trying to connect to dnsseeder at {}'.format(deregister_url))

        try:
            http.post(deregister_url, {'port': config.get('port')})
            logger.info('deregistered with dnsseeder')
        except:
            logger.info('could not deregister with dnsseeder')

network = Network()