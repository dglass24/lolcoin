from .node import Node
from .config import Config
import requests
import json

class Network:
    def __init__(self):
        self.peer_nodes = [Node('http://127.0.0.1:5555'), Node('http://127.0.0.1:5000')]

        config = Config()
        for peer_node in self.peer_nodes:
            # server will remove itself from peer network list
            if peer_node.url == 'http://{}:{}'.format(config.get_option('host'), config.get_option('port')):
                self.peer_nodes.remove(peer_node)

        print self.peer_nodes


    def get_nodes(self):
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
            requests.post(node.url + '/blockchainupdate', json=json.dumps(blockchain_list))