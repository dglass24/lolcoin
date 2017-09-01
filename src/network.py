from .config import Config
from .logger import logger
import requests
import json

config = Config()

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

    def broadcast(self, blockchain):
        # the blockchain is a list of Block objects. Convert the blockchain to a list of dictionaries
        # so we can serialize the blockchain to json
        #
        # TODO: Find better way to serialize list of Block objects to json
        #
        blockchain_list = []
        for block in blockchain:
            blockchain_list.append({
                'index': block.index,
                'timestamp': str(block.timestamp),
                'data': block.data,
                'hash': block.hash
            })

        for node in self.get_nodes():
            requests.post(node + '/blockchainupdate', json=json.dumps(blockchain_list))

    def register_with_dnsseeder(self):
        register_url = '{}/register'.format(config.get('dnsseeder_url'))
        logger.info('registering with dnsseeder at {}'.format(register_url))

        peers = requests.post(register_url, headers={'Referer': config.get_host_url()}).content
        peers = json.loads(peers)

        logger.info('registered with dnsseeder')
        logger.info('received {} peer nodes from dnsseeder'.format(len(peers)))

        if len(peers) == 0:
            return

        self.add_nodes(peers)