from flask import Flask
from flask import request
from flask import jsonify
from src.config import Config
from src.logger import logger

import requests
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
            try:
                peer_url = 'http://' + peer + '/addhost'
                requests.post(peer_url, json=json.dumps({'host': node}))
                logger.info('notified peer {} about new node {}'.format(peer_url, node))
            except Exception, e:
                logger.info('could not notify peer {} about new node {}'.format(peer_url, node))
                logger.error('Exception message: '+ str(e))

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
            try:
                requests.post(peer + '/removehost', json=json.dumps({'host': node}))
            except:
                # TODO: log failure
                pass

        return 'ok'

if __name__ == '__main__':
    node.run(host=config.get('dnsseeder_host'), port=config.get('dnsseeder_port'))











