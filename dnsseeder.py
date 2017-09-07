from flask import Flask
from flask import request
from flask import jsonify
from src.config import Config
from src.logger import logger

import src.http as http
import json

node = Flask(__name__)

config = Config()

peers = set()

@node.route('/ping', methods=['GET'])
def get_ping():
    return 'pong\n'

@node.route('/register', methods=['POST'])
def post_register():
    if request.method == 'POST':
        data = json.loads(request.get_json(force=True))
        node = '{}:{}'.format(request.remote_addr, data['port'])

        existing_peers = peers.copy()
        existing_peers.discard(node)
        peers.add(node)

        logger.info('registered node {}'.format(node))

        # broadcast new peer to all existing peers
        for peer in existing_peers:
            peer_url = 'http://{}/addhost'.format(peer)
            try:
                http.post(peer_url, {'host': node})
                logger.info('notified peer {} about new node {}'.format(peer_url, node))
            except Exception, e:
                logger.info('could not notify peer {} about new node {}'.format(peer_url, node))

        return jsonify(list(existing_peers))

@node.route('/deregister', methods=['POST'])
def post_deregister():
    if request.method == 'POST':
        data = json.loads(request.get_json(force=True))
        node = '{}:{}'.format(request.remote_addr, data['port'])
        peers.discard(node)

        logger.info('deregistered node {}'.format(node))

        # broadcast new peer to all existing peers
        for peer in peers:
            peer_url = 'http://{}/removehost'.format(peer)
            try:
                http.post(peer_url, {'host': node})
                logger.info('notified peer {} about removed node {}'.format(peer_url, node))
            except:
                logger.info('could not notify peer {} about removed node {}'.format(peer_url, node))

        return 'ok'

if __name__ == '__main__':
    node.run(host=config.get('seed_host'), port=config.get('seed_port'))











