from .config import Config
from .logger import logger
import requests
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

    def broadcast_new_block(self, new_block):
        for node in self.get_nodes():
            requests.post(node + '/newblock',
                          json=new_block.to_json(),
                          headers={'Referer': config.get_host_url()})

    def register_with_dnsseeder(self):
        registered = False

        while not registered:
            register_url = '{}/register'.format(config.get('dnsseeder_url'))
            logger.info('trying to connect to dnsseeder at {}'.format(register_url))

            try:
                peers = requests.post(register_url, headers={'Referer': config.get_host_url()}).content
                peers = json.loads(peers)
                registered = True
            except:
                logger.info('could not connect to dnsseeder, retrying in 30 seconds')
                time.sleep(30)


        logger.info('registered with dnsseeder')
        logger.info('received {} peer nodes from dnsseeder'.format(len(peers)))

        if len(peers) == 0:
            return

        self.add_nodes(peers)

config = Config()
network = Network()