from .node import Node
from .config import Config
import requests
import json

config = Config()

class Network:
    def __init__(self):
        self.peer_nodes = []

    def get_nodes(self):
        return self.peer_nodes

    def add_node(self, node):
        self.peer_nodes.append(node)
        print 'adding node {}'.format(node)
        print 'now nodes are:'
        print self.peer_nodes

        return self.peer_nodes

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
        data = requests.post('{}/register'.format(config.get('dnsseeder_url')),
                             headers={'Referer': config.get_host_url()}).content
        data = json.loads(data)
        print data
        self.peer_nodes = data

        # TODO: Log which peers were added